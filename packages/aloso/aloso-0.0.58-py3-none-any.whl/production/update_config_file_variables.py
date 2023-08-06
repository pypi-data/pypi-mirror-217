import os

from output.shell.configs_shell import ConfigsShell


def find_sample_file(env_folder_path):
    for root, dirs, files in os.walk(env_folder_path):
        for file in files:
            if file == 'config_sample.py':
                return os.path.join(root, file)
    return None


if __name__ == "__main__":
    project_root = os.path.abspath(os.getcwd())
    env_folder = os.path.join(project_root, 'env')
    config_sample_path = find_sample_file(env_folder)
    config_file_path = os.path.join(project_root, "config.py")

    try:
        print("\033[1m\033[32mMise à jour du fichier de configuration en cours...\033[0m")
        ConfigsShell.update_production_config_file(sample_file_path=config_sample_path,
                                                   config_file_path_to_update=config_file_path)
        print("\033[1m\033[32mMise à jour terminée\033[0m")
    except Exception as e:
        print(f"\033[1m\033[31mErreur lors de la mise à jour: {e}\033[0m")
