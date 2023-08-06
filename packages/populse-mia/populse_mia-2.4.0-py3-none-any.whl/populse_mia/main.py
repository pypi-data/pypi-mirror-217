# -*- coding: utf-8 -*-
"""The first module used at the mia runtime.

Basically, this module is dedicated to the initialisation of the basic
parameters and the various checks necessary for a successful launch of the
mia's GUI.

:Contains:
    :Class:
        - PackagesInstall

    :Function:
        - launch_mia
        - main
        - verify_processes

"""

###############################################################################
# Populse_mia - Copyright (C) IRMaGe/CEA, 2018
# Distributed under the terms of the CeCILL license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html
# for details.
###############################################################################

import copy
import inspect
import os
import pkgutil
import sys
import traceback
from functools import partial
from pathlib import Path

import yaml
from packaging import version

# PyQt5 imports
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QLockFile, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

pypath = []

# Disables any etelemetry check.
if "NO_ET" not in os.environ:
    os.environ["NO_ET"] = "1"

if "NIPYPE_NO_ET" not in os.environ:
    os.environ["NIPYPE_NO_ET"] = "1"

# General QApplication class instantiation
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QApplication(sys.argv)
QApplication.setOverrideCursor(Qt.WaitCursor)

# Adding the populse projects path to sys.path, if in developer mode
if (
    not os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    in sys.path
):  # "developer" mode
    DEV_MODE = True
    root_dev_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    )
    branch = ""
    populse_bdir = ""
    capsul_bdir = ""
    soma_bdir = ""

    if not os.path.isdir(os.path.join(root_dev_dir, "populse_mia")):
        # Different sources layout - try casa_distro mode
        root_dev_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
        )

        if os.path.basename(root_dev_dir) == "populse":
            root_dev_dir = os.path.dirname(root_dev_dir)
            populse_bdir = "populse"
            soma_bdir = "soma"

        print("root_dev_dir:", root_dev_dir)
        branch = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        print("branch:", branch)

    i = 0
    # Adding populse_mia
    print('\n- Mia in "developer" mode')
    mia_dev_dir = os.path.join(
        root_dev_dir, populse_bdir, "populse_mia", branch
    )
    print("  . Using populse_mia package from {} ...".format(mia_dev_dir))
    sys.path.insert(i, mia_dev_dir)
    pypath.append(mia_dev_dir)
    del mia_dev_dir
    from populse_mia import info

    print(f"    populse_mia version: {info.__version__}")

    # Adding capsul
    if os.path.isdir(os.path.join(root_dev_dir, capsul_bdir, "capsul")):
        i += 1
        capsul_dev_dir = os.path.join(
            root_dev_dir, capsul_bdir, "capsul", branch
        )
        print("  . Using capsul package from {} ...".format(capsul_dev_dir))
        sys.path.insert(i, capsul_dev_dir)
        pypath.append(capsul_dev_dir)
        del capsul_dev_dir

    else:
        try:
            import capsul

        except Exception:
            pass

        else:
            capsul_dir = os.path.dirname(os.path.dirname(capsul.__file__))
            print("  . Using capsul package from {} ...".format(capsul_dir))
            del capsul_dir
            del capsul

    # Adding soma_base:
    if os.path.isdir(os.path.join(root_dev_dir, soma_bdir, "soma-base")):
        i += 1
        soma_b_dev_dir = os.path.join(
            root_dev_dir, soma_bdir, "soma-base", branch, "python"
        )
        print("  . Using soma package from {} ...".format(soma_b_dev_dir))
        sys.path.insert(i, soma_b_dev_dir)
        pypath.append(soma_b_dev_dir)
        del soma_b_dev_dir

    else:
        import soma

        soma_b_dir = os.path.dirname(os.path.dirname(soma.__file__))
        print("  . Using soma package from {} ...".format(soma_b_dir))
        del soma_b_dir
        del soma

    # Adding soma_workflow:
    if os.path.isdir(os.path.join(root_dev_dir, soma_bdir, "soma-workflow")):
        i += 1
        soma_w_dev_dir = os.path.join(
            root_dev_dir, soma_bdir, "soma-workflow", branch, "python"
        )
        print(
            "  . Using soma_workflow package from {} "
            "...".format(soma_w_dev_dir)
        )
        sys.path.insert(i, soma_w_dev_dir)
        pypath.append(soma_w_dev_dir)
        del soma_w_dev_dir

    else:
        import soma_workflow

        soma_w_dir = os.path.dirname(os.path.dirname(soma_workflow.__file__))
        print("  . Using soma_worflow package from {} ...".format(soma_w_dir))
        del soma_w_dir
        del soma_workflow

    # Adding populse_db:
    if os.path.isdir(os.path.join(root_dev_dir, populse_bdir, "populse_db")):
        i += 1
        populse_db_dev_dir = os.path.join(
            root_dev_dir, populse_bdir, "populse_db", branch, "python"
        )
        print(
            "  . Using populse_db package from {} "
            "...".format(populse_db_dev_dir)
        )
        sys.path.insert(i, populse_db_dev_dir)
        pypath.append(populse_db_dev_dir)
        del populse_db_dev_dir

    else:
        import populse_db

        populse_db_dir = os.path.dirname(os.path.dirname(populse_db.__file__))
        print(
            "  . Using populse_db package from {} ...".format(populse_db_dir)
        )
        del populse_db_dir
        del populse_db

    # Adding mia_processes:
    if os.path.isdir(
        os.path.join(root_dev_dir, populse_bdir, "mia_processes")
    ):
        i += 1
        mia_processes_dev_dir = os.path.join(
            root_dev_dir, populse_bdir, "mia_processes", branch
        )
        print(
            "  . Using mia_processes package from {} "
            "...".format(mia_processes_dev_dir)
        )
        sys.path.insert(i, mia_processes_dev_dir)
        pypath.append(mia_processes_dev_dir)
        del mia_processes_dev_dir

    else:
        try:
            import mia_processes

        except Exception:
            pass

        else:
            mia_processes_dir = os.path.dirname(
                os.path.dirname(mia_processes.__file__)
            )
            print(
                "  . Using mia_processes package from {} "
                "...".format(mia_processes_dir)
            )
            del mia_processes_dir
            del mia_processes

    # Adding personal libraries (User_processes: by default in Mia, but others
    # can be added by developers):
    # TODO: The same fix type will certainly have to be made in user more
    #        (for ~/.populse_mia/process' ).
    mia_proc = os.path.join(
        root_dev_dir, populse_bdir, "populse_mia", "processes"
    )

    if os.path.isdir(mia_proc):
        mia_proc_dir = os.listdir(mia_proc)

        if mia_proc_dir:
            i += 1
            sys.path.insert(i, mia_proc)
            pypath.append(mia_proc)

            for elt in mia_proc_dir:
                print(
                    "  . Using {0} package from {1}...".format(elt, mia_proc)
                )

        del mia_proc_dir

        try:
            del elt

        except NameError:
            # there is nothing in the "processes" directory!
            os.mkdir(os.path.join(mia_proc, "User_processes"))
            Path(
                os.path.join(mia_proc, "User_processes", "__init__.py")
            ).touch()

    del mia_proc
    del root_dev_dir

elif "CASA_DISTRO" in os.environ:
    # If the casa distro development environment is detected, developer mode
    # is activated.
    DEV_MODE = True

else:  # "user" mode
    DEV_MODE = False
    print('\n- Mia in "user" mode')

# Check if nipype and mia_processes and capsul are available on the station.
# If not available ask the user to install them
pkg_error = []
# pkg_error: a list containing nipype and/or mia_processes and/or capsul, if
#            not currently installed
capsulVer = None  # capsul version currently installed
miaProcVer = None  # mia_processes version currently installed
nipypeVer = None  # nipype version currently installed

try:
    from capsul import info as capsul_info

    capsulVer = capsul_info.__version__

except (ImportError, AttributeError) as e:
    pkg_error.append("capsul")
    print("\n" + "*" * 37)
    print("MIA warning {0}: {1}".format(e.__class__, e))
    print("*" * 37 + "\n")

try:
    __import__("nipype")
    nipypeVer = sys.modules["nipype"].__version__

except (ImportError, AttributeError) as e:
    pkg_error.append("nipype")
    print("\n" + "*" * 37)
    print("MIA warning {0}: {1}".format(e.__class__, e))
    print("*" * 37 + "\n")

try:
    __import__("mia_processes")
    miaProcVer = sys.modules["mia_processes"].__version__

except (ImportError, AttributeError) as e:
    pkg_error.append("mia_processes")
    print("\n" + "*" * 37)
    print("MIA warning {0}: {1}".format(e.__class__, e))
    print("*" * 37 + "\n")

if len(pkg_error) > 0:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("populse_mia -  warning: ImportError!")

    if len(pkg_error) == 1:
        msg.setText(
            "An issue has been detected with the {0} package. "
            "Please (re)install this package and/or fix the "
            "problems displayed in the standard output. "
            "Then, start again Mia ...".format(pkg_error[0])
        )

    elif len(pkg_error) == 2:
        msg.setText(
            "An issue has been detected with the {0} and {1} packages. "
            "Please (re)install these package and/or fix the "
            "problems displayed in the standard output. "
            "Then, start again Mia ...".format(pkg_error[0], pkg_error[1])
        )

    else:
        msg.setText(
            "An issue has been detected with the {0}, {1} and {2} packages. "
            "Please (re)install these package and/or fix the "
            "problems displayed in the standard output. "
            "Then, start again Mia ...".format(
                pkg_error[0], pkg_error[1], pkg_error[2]
            )
        )

    msg.setStandardButtons(QMessageBox.Ok)
    msg.buttonClicked.connect(msg.close)
    msg.exec()
    sys.exit(1)

# Now that populse projects paths have been, if necessary, added
# to sys.path, we can import these projects:

# capsul imports
import capsul.api as capsul_api  # noqa E402
from capsul.api import get_process_instance  # noqa E402

# soma-base imports
from soma.qt_gui.qtThread import QtThreadCall  # noqa E402

# populse_mia imports
from populse_mia.data_manager.project import Project  # noqa E402
from populse_mia.data_manager.project_properties import (  # noqa E402
    SavedProjects,
)
from populse_mia.software_properties import Config  # noqa E402
from populse_mia.user_interface.main_window import MainWindow  # noqa E402
from populse_mia.utils.utils import check_python_version  # noqa E402

main_window = None


class PackagesInstall:
    """Help to make available a pipeline package in the Mia pipeline library,
    in a recursive way.

    :Contains:
        :Method:
            - __init__: constructor
            - add_package: provide recursive representation of a package
    """

    _already_loaded = {  # these classes should not appear
        # in available processes
        "mia_processes.process_matlab.ProcessMatlab",
        "populse_mia.user_interface.pipeline_manager.process_mia.ProcessMIA",
        "capsul.process.process.Process",
        "capsul.process.process.NipypeProcess",
        "capsul.process.process.FileCopyProcess",
        "capsul.pipeline.pipeline_nodes.ProcessNode",
        "capsul.pipeline.pipeline_nodes.PipelineNode",
        "capsul.pipeline.pipeline_nodes.Node",
    }

    def __init__(self):
        """Initialise the packages instance attribute."""

        self.packages = {}

    def add_package(self, module_name, class_name=None):
        """Provide recursive representation of a package and its
        subpackages/modules, to construct the Mia's pipeline library.

        :param module_name: name of the module to add in the pipeline library
        :param class_name: only this pipeline will be added to the pipeline
                           library (optional)
        :return: dictionary of dictionaries containing
                 package/subpackages/pipelines status.
                 ex: {package: {subpackage: {pipeline: 'process_enabled'}}}
        """

        # (filter out test modules)
        if (
            module_name
            and "test" not in module_name.split(".")
            and "tests" not in module_name.split(".")
        ):
            # reloading the package
            if module_name in sys.modules.keys():
                del sys.modules[module_name]

            try:
                __import__(module_name)
                pkg = sys.modules[module_name]

                for k, v in sorted(list(pkg.__dict__.items())):
                    if class_name and k != class_name:
                        continue

                    # checking each class in the package
                    if inspect.isclass(v):
                        if v in PackagesInstall._already_loaded:
                            continue

                        if hasattr(v, "__module__"):
                            vname = "%s.%s" % (v.__module__, v.__name__)

                        elif hasattr(v, "__package__"):
                            vname = "%s.%s" % (v.__package__, v.__name__)

                        else:
                            print("no module nor package for", v)
                            vname = v.__name__

                        if vname in PackagesInstall._already_loaded:
                            continue

                        PackagesInstall._already_loaded.add(vname)

                        try:
                            try:
                                get_process_instance(
                                    "%s.%s" % (module_name, v.__name__)
                                )

                            except Exception:
                                if v is capsul_api.Node or not issubclass(
                                    v, capsul_api.Node
                                ):
                                    raise

                            # updating the tree's dictionary
                            path_list = module_name.split(".")
                            path_list.append(k)
                            pkg_iter = self.packages

                            for element in path_list:
                                if element in pkg_iter.keys():
                                    pkg_iter = pkg_iter[element]

                                else:
                                    if element is path_list[-1]:
                                        pkg_iter[element] = "process_enabled"
                                        print("Detected brick: ", element)

                                    else:
                                        pkg_iter[element] = {}
                                        pkg_iter = pkg_iter[element]

                        except Exception:
                            pass

                # check if there are subpackages, in this case explore them
                path = getattr(pkg, "__path__", None)

                if (
                    path is None
                    and hasattr(pkg, "__file__")
                    and os.path.basename(pkg.__file__).startswith("__init__.")
                ):
                    path = [os.path.dirname(pkg.__file__)]

                if path:
                    for _, modname, ispkg in pkgutil.iter_modules(path):
                        if modname == "__main__":
                            continue  # skip main

                        print(
                            "\nExploring subpackages of "
                            "{0}: {1} ...".format(
                                module_name, str(module_name + "." + modname)
                            )
                        )
                        self.add_package(
                            str(module_name + "." + modname), class_name
                        )

            except Exception as e:
                print(
                    "\nWhen attempting to add a package and its modules to "
                    "the package tree, the following exception was caught:"
                )
                print("{0}".format(e))

            return self.packages


def launch_mia():
    """Actual launch of the Mia software.

    Overload the sys.excepthook handler with the _my_excepthook private
    function. Check if the software is already opened in another instance.
    If not, the list of opened projects is cleared. Checks if saved projects
    known in the Mia software still exist, and updates if necessary.
    Instantiates a 'project' object that handles projects and their
    associated database and finally launch of the Mia's GUI.

    :Contains:
        :Private function:
            - _my_excepthook: log all uncaught exceptions in non-interactive
              mode
            - _verify_saved_projects: checks if the projects are still existing
    """

    def _my_excepthook(etype, evalue, tback):
        """Log all uncaught exceptions in non-interactive mode.

        All python exceptions are handled by function, stored in
        sys.excepthook. By overloading the sys.excepthook handler with
        _my_excepthook function, this last function is called whenever
        there is an unhandled exception (so one that exits the interpreter).
        We take advantage of it to clean up mia software before closing.

        :param etype: exception class
        :param evalue: exception instance
        :param tback: traceback object

        :Contains:
            :Private function:
                - _clean_up(): cleans up the mia software during "normal"
                  closing.
        """

        def _clean_up():
            """Cleans up Mia software during "normal" closing.

            Make a cleanup of the opened projects just before exiting mia.
            """

            global main_window
            config = Config()
            opened_projects = config.get_opened_projects()

            try:
                opened_projects.remove(main_window.project.folder)
                config.set_opened_projects(opened_projects)
                main_window.remove_raw_files_useless()

            except AttributeError:
                opened_projects = []
                config.set_opened_projects(opened_projects)

            print("\nClean up before closing mia done ...\n")

        # log the exception here
        print("\nException hooking in progress ...")
        _clean_up()
        # then call the default handler
        sys.__excepthook__(etype, evalue, tback)
        # there was some issue/error/problem, so exiting
        sys.exit(1)

    def _verify_saved_projects():
        """Verify if the projects saved in saved_projects.yml file are still
        on the disk.

        :return: the list of the deleted projects
        """

        saved_projects_object = SavedProjects()
        saved_projects_list = copy.deepcopy(saved_projects_object.pathsList)
        deleted_projects = []

        for saved_project in saved_projects_list:
            if not os.path.isdir(saved_project):
                deleted_projects.append(os.path.abspath(saved_project))
                saved_projects_object.removeSavedProject(saved_project)

        return deleted_projects

    global main_window

    # useful for WebEngine
    try:
        # QtWebEngineWidgets need to be imported before QCoreApplication
        # instance is created (used later)
        from soma.qt_gui.qt_backend import QtWebEngineWidgets  # noqa: F401

    except ImportError:
        pass  # QtWebEngineWidgets is not installed

    sys.excepthook = _my_excepthook

    # working from the scripts directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    lock_file = QLockFile(
        QDir.temp().absoluteFilePath("lock_file_populse_mia.lock")
    )

    if not lock_file.tryLock(100):
        # software already opened in another instance
        pass

    else:
        # no instances of the software is opened, the list of opened projects
        # can be cleared
        config = Config()
        config.set_opened_projects([])

    deleted_projects = _verify_saved_projects()
    project = Project(None, True)
    main_window = MainWindow(project, deleted_projects=deleted_projects)
    main_window.setAttribute(Qt.WA_DeleteOnClose | Qt.WA_QuitOnClose)
    main_window.show()

    # make sure to instantiate the QtThreadCall singleton from the main thread
    QtThreadCall()
    app.exec()


def main():
    """Make basic configuration check then actual launch of mia.

    Checks if Mia is called from the site/dist packages (user mode) or from a
    cloned git repository (developer mode). Launches the verify_processes()
    function, then the launch_mia() function (Mia's real launch !!). When
    Mia is exited, if the ~/.populse_mia/configuration.yml exists, sets the
    dev_mode parameter to False.

    - If launched from a cloned git repository ('developer mode'):
        - the mia_path is the cloned git repository.
    - If launched from the site/dist packages ('user mode'):
        - if the file ~/.populse_mia/configuration.yml file is not found or
          does not exist or if the returned mia_path parameter is incorrect,
          a valid mia_path path is requested from the user, in order
          to try to fix a corruption of this file.

    :Contains:
        :Private function:
            - _browse_mia_path: the user define the mia_path parameter
            - _verify_miaConfig: check the config and try to fix if necessary
    """

    def _browse_mia_path(dialog):
        """The user define the mia_path parameter.

        This method, used only if the mia configuration parameters are
        not accessible, goes with the _verify_miaConfig function,
        which will use the value of the mia_path parameter,
        defined here.

        :param dialog: QtWidgets.QDialog object ('msg' in the main function)
        """

        dname = QFileDialog.getExistingDirectory(
            dialog, "Please select MIA path", os.path.expanduser("~")
        )
        dialog.file_line_edit.setText(dname)

    def _verify_miaConfig(dialog=None):
        """Check the config is not corrupted and try to fix if necessary.

        The purpose of this method is twofold. First, it allows to
        update the obsolete values for some parameters of the
        mia_user_path/properties/config.yml file. Secondly, it allows
        to correct the value of the mia_user_path parameter in the
        ~/.populse_mia/configuration.yml file, (in the case of a user
        mode launch, because the developer mode launch does not need
        this parameter).

        In the case of a launch in user mode, this method goes with the
        _browse_mia_path() function, the latter having allowed the
        definition of the mia_user_path parameter, the objective here
        is to check if the value of this parameter is valid. The
        mia_path parameters are saved in the
        ~/.populse_mia/configuration.yml file (the mia_user_path
        parameter is mandatory in the user mode). Then the data in the
        mia_path/properties/config.yml file are checked. If an
        exception is raised during the _verify_miaConfig function, the
        "MIA path selection" window is not closed and the user is
        prompted again to set the mia_user_path parameter.

        :param dialog: QtWidgets.QDialog object ('msg' in the main function)
        """

        save_flag = False

        if DEV_MODE:  # "developer" mode
            try:
                config = Config()

                if not config.get_admin_hash():
                    config.set_admin_hash(
                        "60cfd1916033576b0f2368603fe612fb"
                        "78b8c20e4f5ad9cf39c9cf7e912dd282"
                    )

            except Exception as e:
                print(
                    "\nMIA configuration settings could not be "
                    "recovered: {0} ...".format(e)
                )
                print("\nMIA is exiting ...\n")
                sys.exit(1)

        elif dialog is not None:  # "user" mode only if problem
            mia_home_config = dict()
            mia_home_config["mia_user_path"] = dialog.file_line_edit.text()
            print("\nNew values in ~/.populse_mia/configuration.yml: ")

            for key, value in mia_home_config.items():
                print("- {0}: {1}".format(key, value))

            print()

            with open(dot_mia_config, "w", encoding="utf8") as configfile:
                yaml.dump(
                    mia_home_config,
                    configfile,
                    default_flow_style=False,
                    allow_unicode=True,
                )

            try:
                config = Config()
                if not config.get_admin_hash():
                    config.set_admin_hash(
                        "60cfd1916033576b0f2368603fe612fb"
                        "78b8c20e4f5ad9cf39c9cf7e912dd282"
                    )
                dialog.close()

            except Exception as e:
                print(
                    "\nCould not fetch the "
                    "configuration file: {0} ...".format(
                        e,
                    )
                )
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle(
                    "populse_mia - Error: " "mia path directory incorrect"
                )
                msg.setText(
                    "Error: Please select the MIA path (directory with"
                    "\nthe processes, properties & resources "
                    "directories): "
                )
                msg.setStandardButtons(QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.exec()

        else:  # "user" mode (initial pass)
            config = Config()
            if not config.get_admin_hash():
                config.set_admin_hash(
                    "60cfd1916033576b0f2368603fe612fb"
                    "78b8c20e4f5ad9cf39c9cf7e912dd282"
                )

        if "config" in locals():
            for key, value in config.config.items():
                if value == "no":
                    save_flag = True
                    config.config[key] = False

                if value == "yes":
                    save_flag = True
                    config.config[key] = True

                if save_flag is True:
                    config.saveConfig()

    dot_mia_config = os.path.join(
        os.path.expanduser("~"), ".populse_mia", "configuration.yml"
    )

    if DEV_MODE:  # "developer" mode
        _verify_miaConfig()

    else:  # "user" mode
        try:
            if not os.path.exists(os.path.dirname(dot_mia_config)):
                os.mkdir(os.path.dirname(dot_mia_config))
                print(
                    "\nThe {0} directory is created "
                    "...".format(os.path.dirname(dot_mia_config))
                )

            # Just to check if dot_mia_config file is well readable/writeable
            with open(dot_mia_config, "r") as stream:
                if version.parse(yaml.__version__) > version.parse("5.1"):
                    mia_home_config = yaml.load(stream, Loader=yaml.FullLoader)
                else:
                    mia_home_config = yaml.load(stream)

            with open(dot_mia_config, "w", encoding="utf8") as configfile:
                yaml.dump(
                    mia_home_config,
                    configfile,
                    default_flow_style=False,
                    allow_unicode=True,
                )

        except Exception as e:
            # the configuration.yml file does not exist or has not been
            # correctly read ...
            print(
                "\nA problem has been detected when opening"
                " the ~/.populse_mia/configuration.yml file"
                " or with the parameters returned from this file: ",
                e,
            )

            # open popup, user choose the path to .populse_mia/populse_mia dir
            msg = QDialog()
            msg.setWindowTitle("populse_mia - mia path selection")
            vbox_layout = QVBoxLayout()
            hbox_layout = QHBoxLayout()
            file_label = QLabel(
                "Please select the MIA path (directory with\n "
                "the processes, properties & resources "
                "directories): "
            )
            msg.file_line_edit = QLineEdit()
            msg.file_line_edit.setFixedWidth(400)
            file_button = QPushButton("Browse")
            file_button.clicked.connect(partial(_browse_mia_path, msg))
            vbox_layout.addWidget(file_label)
            hbox_layout.addWidget(msg.file_line_edit)
            hbox_layout.addWidget(file_button)
            vbox_layout.addLayout(hbox_layout)
            hbox_layout = QHBoxLayout()
            msg.ok_button = QPushButton("Ok")
            msg.ok_button.clicked.connect(partial(_verify_miaConfig, msg))
            hbox_layout.addWidget(msg.ok_button)
            vbox_layout.addLayout(hbox_layout)
            msg.setLayout(vbox_layout)
            msg.exec()

        else:
            _verify_miaConfig()

    global pypath

    if DEV_MODE and pypath:
        config = Config()
        config.get_capsul_engine()
        c = config.get_capsul_config()
        pc = (
            c.setdefault("engine", {})
            .setdefault("global", {})
            .setdefault("capsul.engine.module.python", {})
            .setdefault("python", {})
        )
        pc["executable"] = sys.executable
        pc["config_id"] = "python"
        pc["config_environment"] = "global"

        if "path" in pc:
            matches = [
                "capsul",
                "mia_processes",
                "populse_mia",
                os.path.join("populse_db", "python"),
                os.path.join("soma-base", "python"),
                os.path.join("soma-workflow", "python"),
                os.path.join("populse_mia", "processes"),
            ]

            for i in pc["path"]:
                if i not in pypath and not any(x in i for x in matches):
                    pypath.append(i)

        pc["path"] = pypath
        print("\nChanged python conf:", pc)
        config.update_capsul_config()
        config.saveConfig()

    verify_processes()
    check_python_version()
    launch_mia()


def verify_processes():
    """Install or update to the last version available on the station, for
    nipype, capsul and mia_processes processes libraries.

    By default, Mia provides three process libraries in the pipeline library
    (available in Pipeline Manager tab). The nipype, given as it is because
    it is developed by another team (https://github.com/nipy/nipype), and
    mia_processes, capsul which are developed under the umbrella of populse
    (https://github.com/populse/mia_processes). When installing Mia in
    user mode, these three libraries are automatically installed on the
    station. The idea is to use the versioning available with pypi
    (https://pypi.org/). Thus, it is sufficient for the user to change the
    version of the library installed on the station (pip install...) to
    also change the version available in Mia. Indeed, when starting Mia, the
    verify_processes function will install or update nipype and
    mia_processes libraries in the pipeline library. Currently, it is
    mandatory to have nipype, capsul and mia_processes installed in the
    station.
    All this information, as well as the installed versions and package
    paths are saved in the  mia_path/properties/process_config.yml file.
    When an upgrade or downgrade is performed for a package, the last
    configuration used by the user is kept (if a pipeline was visible, it
    remains so and vice versa). However, if a new pipeline is available in
    the new version it is automatically marked as visible in the library.

    :Contains:
        :Private function:
            - _deepCompDic: keep the previous config existing before packages
              update
    """

    def _deepCompDic(old_dic, new_dic):
        """Try to keep the previous configuration existing before the
        update of the packages.

        Recursive comparison of the old_dic and new _dic dictionary. If
        all keys are recursively identical, the final value at the end
        of the whole tree in old_dic is kept in the new _dic. To sum
        up, this function is used to keep up the user display preferences
        in the processes' library of the Pipeline Manager Editor.

        :param old_dic: the dic representation of the previous package
                        configuration
        :param new_dic: the dic representation of the new package configuration
        :return: True if the current level is a pipeline that existed in the
                 old configuration, False if the package/subpackage/pipeline
                 did not exist
        """

        if isinstance(old_dic, str):
            return True

        for key in old_dic:
            if key not in new_dic:
                pass

            # keep the same configuration for the pipeline in new and old dic
            elif _deepCompDic(old_dic[str(key)], new_dic[str(key)]):
                new_dic[str(key)] = old_dic[str(key)]

    othPckg = None
    # othPckg: a list containing all packages, other than nipype, mia_processes
    #          and capsul, used during the previous launch of mia.
    pack2install = []
    # pack2install: a list containing the package (nipype and/or
    #               mia_processes and/or capsul) to install
    proc_content = None
    # proc_content: python dictionary object corresponding to the
    #               process_config.yml property file

    config = Config()
    proc_config = os.path.join(
        config.get_mia_path(), "properties", "process_config.yml"
    )
    print(
        "\nChecking the installed version for nipype, "
        "mia_processes and capsul ..."
    )

    if os.path.isfile(proc_config):
        with open(proc_config, "r") as stream:
            if version.parse(yaml.__version__) > version.parse("5.1"):
                proc_content = yaml.load(stream, Loader=yaml.FullLoader)
            else:
                proc_content = yaml.load(stream)

    if (isinstance(proc_content, dict)) and ("Packages" in proc_content):
        othPckg = [
            f
            for f in proc_content["Packages"]
            if f not in ["mia_processes", "nipype", "capsul"]
        ]

    # Checking that the packages used during the previous launch
    # of mia are still available
    if othPckg:
        for pckg in othPckg:
            try:
                __import__(pckg)

            except ImportError as e:
                # Try to update the sys.path for the processes/ directory
                # currently used
                if (
                    not (
                        os.path.relpath(
                            os.path.join(config.get_mia_path(), "processes")
                        )
                        in sys.path
                    )
                ) and (
                    not (
                        os.path.abspath(
                            os.path.join(config.get_mia_path(), "processes")
                        )
                        in sys.path
                    )
                ):
                    sys.path.append(
                        os.path.abspath(
                            os.path.join(config.get_mia_path(), "processes")
                        )
                    )

                    try:
                        __import__(pckg)

                        # update the Paths parameter (processes/ directory
                        # currently used) saved later in the
                        # mia_path/properties/process_config.yml file
                        if ("Paths" in proc_content) and (
                            isinstance(proc_content["Paths"], list)
                        ):
                            if (
                                not os.path.relpath(
                                    os.path.join(
                                        config.get_mia_path(), "processes"
                                    )
                                )
                                in proc_content["Paths"]
                            ) and (
                                not os.path.abspath(
                                    os.path.join(
                                        config.get_mia_path(), "processes"
                                    )
                                )
                                in proc_content["Paths"]
                            ):
                                proc_content["Paths"].append(
                                    os.path.abspath(
                                        os.path.join(
                                            config.get_mia_path(), "processes"
                                        )
                                    )
                                )

                        else:
                            proc_content["Paths"] = [
                                os.path.abspath(
                                    os.path.join(
                                        config.get_mia_path(), "processes"
                                    )
                                )
                            ]

                        with open(proc_config, "w", encoding="utf8") as stream:
                            yaml.dump(
                                proc_content,
                                stream,
                                default_flow_style=False,
                                allow_unicode=True,
                            )

                        # Finally, the processes' directory currently used is
                        # removed from the sys.path because this directory is
                        # now added to the Paths parameter in the
                        # mia_path/properties/process_config.yml file
                        sys.path.remove(
                            os.path.abspath(
                                os.path.join(
                                    config.get_mia_path(), "processes"
                                )
                            )
                        )

                    # If an exception is raised, ask the user to remove the
                    # package from the pipeline library or reload it
                    except ImportError as e:
                        print("\n{0}".format(e))
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setWindowTitle(
                            "populse_mia - warning: {0}".format(e)
                        )
                        msg.setText(
                            (
                                "At least, {0} has not been found in {1}."
                                "\nTo prevent mia crash when using it, "
                                "please remove (see File > Package "
                                "library manager) or load again (see More"
                                " > Install processes) the corresponding "
                                "process library."
                            ).format(
                                e.msg.split()[-1],
                                os.path.abspath(
                                    os.path.join(
                                        config.get_mia_path(),
                                        "processes",
                                        pckg,
                                    )
                                ),
                            )
                        )
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.buttonClicked.connect(msg.close)
                        msg.exec()
                        sys.path.remove(
                            os.path.abspath(
                                os.path.join(
                                    config.get_mia_path(), "processes"
                                )
                            )
                        )

                # The processes/ directory being already in the sys.path, the
                # package is certainly not properly installed in the processes
                # directory
                else:
                    print("No module named '{0}'".format(pckg))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowTitle("populse_mia - warning: {0}".format(e))
                    msg.setText(
                        (
                            "At least, {0} has not been found in {1}."
                            "\nTo prevent mia crash when using it, "
                            "please remove (see File > Package "
                            "library manager) or load again (see More"
                            " > Install processes) the corresponding "
                            "process library."
                        ).format(
                            e.msg.split()[-1],
                            os.path.abspath(
                                os.path.join(
                                    config.get_mia_path(), "processes"
                                )
                            ),
                        )
                    )
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.buttonClicked.connect(msg.close)
                    msg.exec()

            except SyntaxError as e:
                print(
                    "\nA problem is detected with the '{0}' "
                    "package...\nTraceback:".format(pckg)
                )
                print("".join(traceback.format_tb(e.__traceback__)), end="")
                print("{0}: {1}\n".format(e.__class__.__name__, e))

                txt = (
                    "A problem is detected with the '{0}' package...\n\n"
                    "Traceback:\n{1} {2} \n{3}\n\nThis may lead to a later "
                    "crash of Mia ...\nDo you want Mia tries to fix "
                    "this issue automatically?\nBe careful, risk of "
                    "destruction of the '{4}' module!".format(
                        pckg,
                        "".join(traceback.format_tb(e.__traceback__)),
                        e.__class__.__name__,
                        e,
                        e.filename,
                    )
                )

                lineCnt = txt.count("\n")
                msg = QMessageBox()
                msg.setWindowTitle("populse_mia - warning: {}".format(e))

                if lineCnt > 15:
                    scroll = QScrollArea()
                    scroll.setWidgetResizable(1)
                    content = QWidget()
                    scroll.setWidget(content)
                    layout = QVBoxLayout(content)
                    tmpLabel = QLabel(txt)
                    tmpLabel.setTextInteractionFlags(
                        QtCore.Qt.TextSelectableByMouse
                    )
                    layout.addWidget(tmpLabel)
                    msg.layout().addWidget(
                        scroll, 0, 0, 1, msg.layout().columnCount()
                    )
                    msg.setStyleSheet(
                        "QScrollArea{min-width:550 px; " "min-height: 300px}"
                    )

                else:
                    msg.setText(txt)
                    msg.setIcon(QMessageBox.Warning)

                ok_button = msg.addButton(QMessageBox.Ok)
                msg.addButton(QMessageBox.No)
                msg.exec()

                if msg.clickedButton() == ok_button:
                    with open(e.filename, "r") as file:
                        filedata = file.read()
                        filedata = filedata.replace(
                            "<undefined>", "'<undefined>'"
                        )

                    with open(e.filename, "w") as file:
                        file.write(filedata)

            except ValueError as e:
                print(
                    "\nA problem is detected with the '{0}' "
                    "package...\nTraceback:".format(pckg)
                )
                print("".join(traceback.format_tb(e.__traceback__)), end="")
                print("{0}: {1}\n".format(e.__class__.__name__, e))

                txt = (
                    "A problem is detected with the '{0}' package...\n\n"
                    "Traceback:\n{1} {2} \n{3}\n\nThis may lead to a later "
                    "crash of Mia ...\nPlease, try to fix it !...".format(
                        pckg,
                        "".join(traceback.format_tb(e.__traceback__)),
                        e.__class__.__name__,
                        e,
                    )
                )
                msg = QMessageBox()
                msg.setWindowTitle("populse_mia - warning: {0}".format(e))
                msg.setText(txt)
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.buttonClicked.connect(msg.close)
                msg.exec()

    if (
        (not isinstance(proc_content, dict))
        or (
            (isinstance(proc_content, dict))
            and ("Packages" not in proc_content)
        )
        or (
            (isinstance(proc_content, dict))
            and ("Versions" not in proc_content)
        )
    ):
        # The process_config.yml fle is corrupted or no pipeline/process
        # was available during the previous use of mia or their versions
        # are not known
        pack2install = [
            "nipype.interfaces",
            "mia_processes",
            "capsul.pipeline",
        ]
        old_nipypeVer = None
        old_miaProcVer = None
        old_capsulVer = None

    else:
        # During the previous use of mia, nipype was not available or its
        # version was not known or its version was different from the one
        # currently available on the station
        if (
            (isinstance(proc_content, dict))
            and ("Packages" in proc_content)
            and ("nipype" not in proc_content["Packages"])
        ):
            old_nipypeVer = None
            pack2install.append("nipype.interfaces")

            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("nipype" in proc_content["Versions"])
            ):
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the current nipype "
                    "processes library again in mia ..."
                )

        else:
            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and (proc_content["Versions"] is None)
            ) or (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("nipype" in proc_content["Versions"])
                and (proc_content["Versions"]["nipype"] is None)
            ):
                old_nipypeVer = None
                pack2install.append("nipype.interfaces")
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the nipype processes "
                    "library again in mia ..."
                )

            elif (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("nipype" in proc_content["Versions"])
                and (proc_content["Versions"]["nipype"] != nipypeVer)
            ):
                old_nipypeVer = proc_content["Versions"]["nipype"]
                pack2install.append("nipype.interfaces")

        # During the previous use of mia, mia_processes was not available or
        # its version was not known or its version was different from the one
        # currently available on the station
        if (
            (isinstance(proc_content, dict))
            and ("Packages" in proc_content)
            and ("mia_processes" not in proc_content["Packages"])
        ):
            old_miaProcVer = None
            pack2install.append("mia_processes")

            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("mia_processes" in proc_content["Versions"])
            ):
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the mia_processes "
                    "processes library again in mia ..."
                )

        else:
            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and (proc_content["Versions"] is None)
            ) or (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("mia_processes" in proc_content["Versions"])
                and (proc_content["Versions"]["mia_processes"] is None)
            ):
                old_miaProcVer = None
                pack2install.append("mia_processes")
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the mia_processes "
                    "processes library again in mia ..."
                )

            elif (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("mia_processes" in proc_content["Versions"])
                and (proc_content["Versions"]["mia_processes"] != miaProcVer)
            ):
                old_miaProcVer = proc_content["Versions"]["mia_processes"]
                pack2install.append("mia_processes")

        # During the previous use of mia, capsul was not available or
        # its version was not known or its version was different from the one
        # currently available on the station
        if (
            (isinstance(proc_content, dict))
            and ("Packages" in proc_content)
            and ("capsul" not in proc_content["Packages"])
        ):
            old_capsulVer = None
            pack2install.append("capsul.pipeline")

            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("capsul" in proc_content["Versions"])
            ):
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the capsul "
                    "processes library again in mia ..."
                )

        else:
            if (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and (proc_content["Versions"] is None)
            ) or (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("capsul" in proc_content["Versions"])
                and (proc_content["Versions"]["capsul"] is None)
            ):
                old_capsulVer = None
                pack2install.append("capsul.pipeline")
                print(
                    "\nThe process_config.yml file seems to be corrupted! "
                    "Let's try to fix it by installing the capsul "
                    "processes library again in mia ..."
                )

            elif (
                (isinstance(proc_content, dict))
                and ("Versions" in proc_content)
                and ("capsul" in proc_content["Versions"])
                and (proc_content["Versions"]["capsul"] != capsulVer)
            ):
                old_capsulVer = proc_content["Versions"]["capsul"]
                pack2install.append("capsul.pipeline")

    final_pckgs = dict()  # final_pckgs: the final dic of dic with the
    final_pckgs["Packages"] = {}  # informations about the installed packages,
    final_pckgs["Versions"] = {}  # their versions, and the path to access them

    for pckg in pack2install:
        package = PackagesInstall()

        if "nipype" in pckg:  # Save the packages version
            final_pckgs["Versions"]["nipype"] = nipypeVer

            if old_nipypeVer is None:
                print(
                    "\n\n** Installation in mia of the {0} processes "
                    "library, {1} version ...".format(pckg, nipypeVer)
                )

            else:
                print(
                    "\n\n** Upgrading of the {0} processes library, "
                    "from {1} to {2} version ...".format(
                        pckg, old_nipypeVer, nipypeVer
                    )
                )

        if "mia_processes" in pckg:
            final_pckgs["Versions"]["mia_processes"] = miaProcVer

            if old_miaProcVer is None:
                print(
                    "\n\n** Installation in mia of the {0} processes "
                    "library, {1} version ...".format(pckg, miaProcVer)
                )

            else:
                print(
                    "\n\n** Upgrading of the {0} processes library, "
                    "from {1} to {2} version ...".format(
                        pckg, old_miaProcVer, miaProcVer
                    )
                )

        if "capsul" in pckg:
            final_pckgs["Versions"]["capsul"] = capsulVer

            if old_capsulVer is None:
                print(
                    "\n\n** Installation in mia of the {0} processes "
                    "library, {1} version ...".format(pckg, capsulVer)
                )

            else:
                print(
                    "\n\n** Upgrading of the {0} processes library, "
                    "from {1} to {2} version ...".format(
                        pckg, old_capsulVer, capsulVer
                    )
                )

        print("\nExploring {0} ...".format(pckg))
        pckg_dic = package.add_package(pckg)
        # pckg_dic: a dic of dic representation of a package and its
        #           subpackages/modules
        #           Ex. {package: {subpackage: {pipeline:'process_enabled'}}}

        for item in pckg_dic:
            final_pckgs["Packages"][item] = pckg_dic[item]

    if pack2install:
        if len(pack2install) == 2:
            if not any("nipype" in s for s in pack2install):
                print(
                    "\n** The nipype processes library in mia is "
                    "already using the current installed version ({0}) "
                    "for this station\n".format(nipypeVer)
                )

            elif not any("mia_processes" in s for s in pack2install):
                print(
                    "\n** The mia_processes library in mia is "
                    "already using the current installed version ({0}) "
                    "for this station\n".format(miaProcVer)
                )

            elif not any("capsul" in s for s in pack2install):
                print(
                    "\n** The capsul library in mia is "
                    "already using the current installed version ({0}) "
                    "for this station\n".format(capsulVer)
                )

        elif len(pack2install) == 1:
            if any("nipype" in s for s in pack2install):
                print(
                    "\n** The mia_processes and capsul processes "
                    "libraries are already using in mia the current "
                    "installed version ({0} and {1} respectively) for "
                    "this station\n".format(miaProcVer, capsulVer)
                )

            elif any("mia_processes" in s for s in pack2install):
                print(
                    "\n** The nipype and capsul processes "
                    "libraries are already using in mia the current "
                    "installed version ({0} and {1} respectively) for "
                    "this station\n".format(nipypeVer, capsulVer)
                )

            elif any("capsul" in s for s in pack2install):
                print(
                    "\n** The mia_processes and nipype processes "
                    "libraries are already using in mia the current "
                    "installed version ({0} and {1} respectively) for "
                    "this station\n".format(miaProcVer, nipypeVer)
                )

        if (isinstance(proc_content, dict)) and ("Paths" in proc_content):
            # Save the path to the packages
            final_pckgs["Paths"] = proc_content["Paths"]

        if (isinstance(proc_content, dict)) and ("Versions" in proc_content):
            if proc_content["Versions"] is None:
                for k in ("nipype", "mia_processes", "capsul"):
                    if k not in final_pckgs["Versions"]:
                        final_pckgs["Versions"][k] = None

            else:
                for item in proc_content["Versions"]:
                    if item not in final_pckgs["Versions"]:
                        final_pckgs["Versions"][item] = proc_content[
                            "Versions"
                        ][item]

        # Try to keep the previous configuration before the update
        # of the packages
        if (isinstance(proc_content, dict)) and ("Packages" in proc_content):
            _deepCompDic(proc_content["Packages"], final_pckgs["Packages"])

            for item in proc_content["Packages"]:
                if item not in final_pckgs["Packages"]:
                    final_pckgs["Packages"][item] = proc_content["Packages"][
                        item
                    ]

        with open(proc_config, "w", encoding="utf8") as stream:
            yaml.dump(
                final_pckgs,
                stream,
                default_flow_style=False,
                allow_unicode=True,
            )

    else:
        print(
            "\n** mia is already using the current installed version of "
            "nipype, mia_processes and capsul for this station ({0}, {1} "
            "and {2}, respectively)\n".format(nipypeVer, miaProcVer, capsulVer)
        )


if __name__ == "__main__":
    # this will only be executed when this module is run directly
    main()
