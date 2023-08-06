def edit_index(name, index_path):
    content = f"""
Welcome to {name} documentation!
===================================

Check out the :doc:`user_guide/index` for the installation instruction.
Check out the :doc:`reference/index` for the documentation.

.. toctree::
   :hidden:
   :titlesonly:

   user_guide/index
   reference/index
"""
    with open(index_path, "w") as f:
        f.write(content)

