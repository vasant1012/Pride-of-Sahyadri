import os


def delete_files_with_extension(extension, current_dir, dry_run=True):
    """
    Scan all folders from current directory and
    delete files with the given extension.

    :param extension: File extension to delete (e.g., ".txt", ".log")
    :param dry_run: If True, only print files without deleting them
    """
    print(
        f"Scanning '{current_dir}' for files with extension '{extension}'...\n")  # NOQA E501

    deleted_files = []

    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.lower().endswith(extension.lower()):
                file_path = os.path.join(root, file)
                if dry_run:
                    print(f"[DRY RUN] Found: {file_path}")
                else:
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                        deleted_files.append(file_path)
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")

    if dry_run:
        print("\nDry run complete. No files were deleted.")
    else:
        print(f"\nDeletion complete. {len(deleted_files)} file(s) deleted.")


# Example usage:
# Preview files first
delete_files_with_extension(
    ".Identifier", f"{os.getcwd()}", dry_run=False) # NOQA E501

# Then delete for real
# delete_files_with_extension(".log", dry_run=False)
