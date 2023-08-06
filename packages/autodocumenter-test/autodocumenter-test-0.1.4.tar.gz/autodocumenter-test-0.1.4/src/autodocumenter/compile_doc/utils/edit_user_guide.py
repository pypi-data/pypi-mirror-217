def edit_user_guide(file_path):
    content = f"""
User Guide
==========
"""
    with open(file_path, "w") as f:
        f.write(content)

