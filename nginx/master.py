import re
import subprocess

print("Starting NGINX Load Balancer Master...")

def add_container(container):
    global contlist
    contlist.append(container)
    print(f"{container} will be added to the network")

    with open("nginx.conf", "r") as fh:
        lines = fh.readlines()

    x = lines.index('### END OF BACKEND SERVERS ###\n')
    lines.insert(x, f'        server {container}:5000;\n')

    with open("nginx.conf", "w") as fh:
        fh.writelines(lines)
    print(f"{container} has been added to the NGINX configuration")

    subprocess.run(["docker", "run", "-d", "--name", container, "--network", "nginx2app", "app"])
    subprocess.run(["docker", "exec", "nginx", "nginx", "-s", "reload"])

def kill(container):
    global contlist
    contlist.remove(container)
    print(f"{container} is being removed from the network")

    with open("nginx.conf", "r") as fh:
        lines = fh.readlines()

    x = lines.index(f'        server {container}:5000;\n')
    lines.pop(x)

    with open("nginx.conf", "w") as fh:
        fh.writelines(lines)
    print(f"{container} has been removed from the NGINX configuration")

    subprocess.run(["docker", "stop", container])
    subprocess.run(["docker", "rm", container])
    subprocess.run(["docker", "exec", "nginx", "nginx", "-s", "reload"])

def main():
    global contlist 
    contlist = []
    while input("Modify/Exit? (m/e): ").strip().lower() == 'm':
        action = input("Add/Remove? (a/r): ").strip().lower()
        container = input("Enter container name: ").strip()
     
        if action == 'a':
            if container in contlist:
                print(f"{container} is already in the list.")
                continue
            add_container(container)
        elif action == 'r':
            if container in contlist:
                kill(container)
            else:
                print(f"{container} is not in the list.")

if __name__ == "__main__":
    main()