import yaml
import os


def create_deploy_yml():
    # Load the todo.yml file
    path = os.path.dirname(__file__)
    with open(os.path.join(path, "todo.yml"), 'r') as stream:
        try:
            todo = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Tasks for the ansible playbook
    tasks = [
        task_install_packages(todo),
        task_install_python_packages(),
        task_copy_files(todo),
        task_run_scripts(todo)
    ]
    playbook = [{
        'hosts': 'localhost',
        'tasks': tasks
    }]

    # Save the playbook to deploy.yml
    with open(os.path.join(path, "deploy.yml"), 'w') as outfile:
        yaml.dump(playbook, outfile, sort_keys=False, default_flow_style=False)


def task_install_packages(todo):
    # Install packages python3 and nginx
    return {
        'name': 'Install packages',
        'package': {
            'name': todo['server']['install_packages'],
            'state': 'present'
        }
    }


def task_install_python_packages():
    # Install python packages, used in the scripts
    return {
        'name': 'Install Python packages',
        'pip': {
            'name': ['bs4', 'redis'],
            'state': 'present',
        }
    }


def task_copy_files(todo):
    # Copy .py files
    return {
        'name': 'Copy files',
        'copy': {
            'src': '{{ item.src }}',
            'dest': '{{ item.dest }}'
        },
        'loop': [{'src': f'../{file}', 'dest': f'./{file}'} for file in todo['server']['exploit_files']]
    }


def task_run_scripts(todo):
    # Add the run for .py files
    return {
        'name': 'Run scripts',
        'shell': '; '.join([
            'python3 ./exploit.py',
            f"python3 ./consumer.py -e {','.join(todo['bad_guys'])}"
        ])
    }


if __name__ == "__main__":
    create_deploy_yml()
