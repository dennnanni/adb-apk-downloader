import os

apks_dir = "." + os.sep + "final_apks" + os.sep
outputs_dir = "." + os.sep + "outputs" + os.sep

def find_matching_paths(path, second):
    first_smali_paths = get_smali_paths(path)
    second_smali_paths = get_smali_paths(second)
    
    matching_paths = []

    first_paths = []
    second_paths = []

    for path in first_smali_paths:
        first_paths.extend(explore_subdirectories(path))
    
    for path in second_smali_paths:
        second_paths.extend(explore_subdirectories(path))

    for path in first_paths:
        if path in second_paths:
            matching_paths.append(path)

    return list(set(matching_paths))

def explore_subdirectories(directory, maxLevel = 5):
    paths = []
    
    for root, dirs, files in os.walk(directory):
        level = root.count(os.sep) - directory.count(os.sep)
        index = [i for i, x in enumerate(root.split(os.sep)) if "smali" in x][0]
        child = os.sep.join(root.split(os.sep)[index + 1:])

        if level <= maxLevel:
            paths.append(child)
            
    return paths

def get_smali_paths(directory, prefix = "smali"):
    paths = []
    
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.startswith(prefix):
                paths.append(os.path.join(root, dir))
    
    return paths

# Example usage
dir_list = [d for d in os.listdir(apks_dir) if os.path.isdir(apks_dir + d)]
if not os.path.exists(outputs_dir):
    os.makedirs(outputs_dir)

for i in range(len(dir_list)):
    for j in range(i + 1, len(dir_list)):
        if dir_list[i] != dir_list[j] :
            matching_paths = find_matching_paths(apks_dir + dir_list[i], apks_dir + dir_list[j])

            if len(matching_paths) > 0:
                effective = 0

                filename = dir_list[i] + "-" + dir_list[j]  + ".txt"

                with open(outputs_dir + filename, "w") as file:
                    for path in matching_paths:
                        if os.sep in path:
                            effective += 1
                            file.write(path + "\n")

                print("Effective matches " + filename + ": " + str(effective))



files = [f for f in os.listdir(outputs_dir) if os.path.isfile(f) and f.endswith('.txt')]
all_lines = []

for file in files:
    with open(outputs_dir + file, 'r') as f:
        lines = f.readlines()
        all_lines.extend(lines)
        f.close()

with open("all-matching.txt", "w") as f:
    f.writelines(list(set(all_lines)))
    f.close()

print("Total effective matches: " + str(len(all_lines)))