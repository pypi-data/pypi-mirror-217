# sync.py - handles gitlab syncing
import os
import yaml
import gitlab
import pydantic

from gcln2 import db
from gcln2 import helpers
from gcln2 import yaml_loader

class SchemaServerDefServer(pydantic.BaseModel):
    api_url: str
    git_url: str
    api_key: str

class SchemaServerDef(pydantic.BaseModel):
    server: SchemaServerDefServer
    cache_file: str

class SchemaSyncCfg(pydantic.BaseModel):
    main_server: SchemaServerDef
    servers: list[SchemaServerDef]

class SyncConnector:
    def __init__(self, server_def: SchemaServerDef, master: bool, root_path):
        self.server_def = server_def
        self.master = master
        self.map_uid2project: dict[str, db.Project] = {}
        fn = os.path.join(root_path, server_def.cache_file)
        self.cache = db.Cache.load(fn, allow_missing=True)
        self.gl: gitlab.Gitlab = gitlab.Gitlab(
            server_def.server.api_url,
            private_token=server_def.server.api_key,
            keep_base_url=True,  # important as it might be via ssh tunnel or similar
        )
        self.group_cache: dict[str, gitlab.Group] = {}  # key is path.
                                                        # This is just a cache, not complete set

    def update_cache_from_server(self):
        num_threads = 0
        self.map_uid2project = self.cache.update_cache_from_server(self.gl, num_threads)


class SyncLocalInfo:

    def __init__(self, controlfile):
        d = yaml.load(controlfile, Loader=yaml_loader.IncludeLoader)
        self.root_path = os.path.split(controlfile.name)[0]
        self.cfg_sync = SchemaSyncCfg(**d)

        self.repos_path = os.path.join(self.root_path, "repos")
        if not os.path.exists(self.repos_path):
            os.mkdir(self.repos_path)



def create_project(
    sli: SyncLocalInfo, c_from: SyncConnector, c_to: SyncConnector, uid: str
):
    src_proj = c_from.map_uid2project[uid]
    if not src_proj.main_branch:
        print(
            f"Project f{src_proj.full_path} doesn't have a main/master branch - ignore it"
        )
        return
    if src_proj.is_home:
        print(f"Project f{src_proj.full_path} is a home - ignore it")
        return

    if not "/" in src_proj.full_path:
        return  #  skip root projects

    # src_proj_nr: int = src_proj.project_id
    namespace = src_proj.full_path.rsplit("/", maxsplit=1)[0]
    names = src_proj.full_name.split("/")
    print(namespace)

    # parent_group = c_from.gl.namespaces.get(namespace)
    # print(parent_group)

    # TODO: should also consider renames of namespaces... Maybe need to cache them? Or just heuristics? Ie, if a known project has another namespace, compare with master server.
    # if all projects in the namespaces matches projects on sync server/old path, then rename?
    splt = namespace.split("/")
    path = ""
    parent_group = None
    for i, s in enumerate(splt):
        if path:
            path += "/"
        path += s
        if path in c_to.group_cache:
            parent_group = c_to.group_cache[path]
            continue
        try:
            parent_group = c_to.group_cache[path] = c_to.gl.namespaces.get(path)
        except gitlab.exceptions.GitlabGetError:
            # not available on target server
            print("Not in target, need to create namespace first", path)
            if not parent_group:
                print("create group", s, names[i])
                group = c_to.gl.groups.create({"name": names[i], "path": s})
            else:
                print("create group", s, names[i], parent_group)
                group = c_to.gl.groups.create(
                    {
                        "name": names[i],
                        "path": s,
                        "parent_id": parent_group.get_id(),
                    }
                )
            parent_group = c_to.group_cache[path] = group

    #  have the parent group. Now create the project
    name = src_proj.full_name.split("/")[-1]
    path = src_proj.full_path.split("/")[-1]

    if path[0] in "_" or path[-1] in "_":
        print(f"Must change path {src_proj.full_path}, invalid with newer gitlabs")
        return

    local_path = os.path.join(sli.repos_path, src_proj.uid)
    if not os.path.exists(local_path):
        # no local copy of the project, so cannot push it up. Then don't create it either
        return

    print(f"Create project on server {path} with name {name}")
    try:
        gl_project = c_to.gl.projects.create(
            {"name": name, "namespace_id": parent_group.get_id(), "path": path}
        )
    except:
        print("*" * 80)
        print(f"ERROR: couldn't create project {src_proj.full_path} {name} {path}")
        print("*" * 80)
        return
    print(f"** Create project {name} {path}")
    url = c_to.server_def.server.git_url + "/" + src_proj.full_path + ".git"
    for branch in [src_proj.main_branch, "_config"]:
        ref_spec = f"remotes/origin/{branch}:refs/heads/{branch}"
        helpers.cmd(["git", "push", url, ref_spec], work_dir=local_path)




def main_sync(args):
    sli = SyncLocalInfo(args.controlfile)
    # print(sli.cfg_sync)

    connectors = [SyncConnector(sli.cfg_sync.main_server, True, sli.root_path)]
    for s in sli.cfg_sync.servers:
        c = SyncConnector(s, False, sli.root_path)
        connectors.append(c)

    print(connectors)
    # update cache from servers
    for c in connectors:
        c.update_cache_from_server()
        print("projects:", len(c.cache.projects), len(c.map_uid2project))

    # pull all from server:
    if 0:
        # TODO: need to make this more efficient, ie, use cache to see if somethings changed.
        for c in connectors:
            for uid, proj in c.map_uid2project.items():
                dirpath = os.path.join(sli.repos_path, uid)
                url = c.server_def.server.git_url + "/" + proj.full_path + ".git"

                print(f"Getting {uid}")
                if not os.path.exists(dirpath):
                    helpers.cmd(
                        ["git", "clone", "--bare", url, uid],
                        work_dir=sli.repos_path,
                        retries=1,
                    )
                else:
                    helpers.cmd(
                        ["git", "fetch", url, "*:*"], work_dir=dirpath, retries=1
                    )

    # check cross sync
    for c_from in connectors:
        for c_to in connectors:
            if c_to == c_from:
                continue
            print(
                f"\nCreate project from server {c_from.server_def.server.api_url} to server {c_to.server_def.server.api_url}"
            )
            uids_from = set(c_from.map_uid2project.keys())
            uids_to = set(c_to.map_uid2project.keys())
            missing = uids_from - uids_to
            for count, miss in enumerate(missing):
                print(f"missing {miss}, add it")
                create_project(sli, c_from, c_to, miss)


def local_sync_copy(args):
    print(args)
    sli = SyncLocalInfo(args.sync_ctrlfile)
    print(sli)
    src_cache = db.Cache.load(args.cache_file, allow_missing=False)
    src_root = os.path.abspath(os.path.split(args.cache_file)[0])
    uid_map = src_cache.build_uid_map()
    for uid, proj in uid_map.items():
        print(uid)
        #TODO: need to fix ws replace logic
        src = os.path.join(src_root, proj.full_name)
        dst = os.path.join(sli.repos_path, uid)
        if not os.path.exists(src):
            print("Strange, missing source {src} - ignoring")
            continue
        print(src)
        print(dst)
        if not os.path.exists(dst):
            helpers.cmd(
                ["git", "clone", "--bare", src, uid], work_dir=sli.repos_path, retries=1
            )
            # note we do a fetch too, to make sure we get all branches.
        helpers.cmd(["git", "fetch", src, "*:*"], work_dir=dst, retries=1)

