try:
    import os
except:
    print("Please REINSTALL python or install the os module (python -m install os))")

try:
    from git import Repo
except:
    try:
        os.system("python -m pip install gitpython")
    except:
        pass
    print("Error Please install the gitpython module (python -m pip install gitpython)")


def clone(url="https://github.com/lkgames256/roodkcab.git", clone_path=""):
    if clone_path == "" or clone_path == " " or clone_path is None:
        try:
            clone_path = str(os.getcwd() + "\gitrepo")
            print(clone_path)
        except:
            return "OS module isn't working!"

    if url == "" or url == " " or url == None:
        url = "https://github.com/lkgames256/roodkcab.git"

    Repo.clone_from(url, clone_path)
    return "Cloned Successful"


def check_git_update(url="https://github.com/lkgames256/roodkcab.git", path_to_git_repo="",
                     atm_update=True):  # Use a Thread to run this
    if path_to_git_repo == "" or path_to_git_repo == " ":
        return "Sorry you nedd to specefiy the path to the REPO"

    if url == "" or url == " " or url == None:
        url = "https://github.com/lkgames256/roodkcab.git"

    try:
        repo = Repo(path_to_git_repo)
        repo.remotes.origin.fetch()
        # Check if local repo is behind remote
        local_commit = repo.active_branch.commit.hexsha
        remote_commit = repo.remotes.origin.refs[repo.active_branch.name].commit.hexsha
        if local_commit != remote_commit:
            repo.remotes.origin.pull()
            return "PULLING NEW VERSION COMPLETE"
        else:
            return "YOUR UP TO DATE"
    except:
        return "ERR PLEASE TRY AGAIN"

# pypi-AgENdGVzdC5weXBpLm9yZwIkYjM0MTEyNmMtNjFkZS00ZTFmLWI3NzEtZTEzMGY0N2NiNjE1AAIqWzMsIjAyN2ZkMzIwLWNhMjYtNDdkNS05ZjJiLTI2Y2RkZTEyMjA4MCJdAAAGIBCIsit-jd8KzN9r9We7lo5TJP-wb9CcaRQpA28c-NzP