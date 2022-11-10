import subprocess
import sys

import pkg_resources as pkgrsc
#installedPackagesList = sorted(["%s" % (i.key) for i in installedPackages])
installedPackagesList = {i.key : i.version for i in pkgrsc.working_set}


def installOrUpgradeIfNecessary(module: str):
    module = module.strip().lower()
    if module not in installedPackagesList:
        print(f"\n\n{module} is currently not installed on this system.")
        inp = input('Do you wish to install now (y/n) ? ').upper().strip()
        if inp == 'Y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", module, "--user"])
        elif inp == 'N':
            print(f"you chose not to install {module}.\n")
        else: print("invalid input.\n")
    else:
        print(f"\nyou already have {module} version {installedPackagesList[module]} installed.")
        inp = input('do you wish to upgrade to a latest version if available (y/n) ? ').upper().strip()
        if inp == 'Y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", module, "--upgrade", "--user"])
            print(f"now you have {module} version {installedPackagesList[module]} installed.")
        elif inp == 'N': print(f"you chose not to upgrade {module}.\n")
        else: print("invalid input.\n")

if __name__ == "__main__":
    necessaryModules = [x for x in input("\nenter the required modules/libraries: ").split()]
    for module in necessaryModules:
        installOrUpgradeIfNecessary(module)