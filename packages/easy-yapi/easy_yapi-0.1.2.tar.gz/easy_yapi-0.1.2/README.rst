=========
easy-yapi
=========


.. image:: https://img.shields.io/pypi/v/easy_yapi.svg
        :target: https://pypi.python.org/pypi/easy_yapi

.. image:: https://img.shields.io/travis/nocoding126/easy_yapi.svg
        :target: https://travis-ci.com/nocoding126/easy_yapi

.. image:: https://readthedocs.org/projects/easy-yapi/badge/?version=latest
        :target: https://easy-yapi.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Yapi Python SDK


* Free software: MIT license
* Documentation:

Installation and Usage
----------------------
.. code-block:: python

   pip install easy_yapi

示例-login
----------
.. code-block:: python

    from easy_yapi import Yapi


    yapi = Yapi(base_url='http://82.156.152.141:3000')
    res = yapi.login(email='nocoding@126.com', password='ymfe.org')
    print(res.text)


Features
--------

* 该库主要用于快速生成yapi接口文档
* 该库是一个练习项目，并未完全实现所有Yapi接口的封装
* 已实现功能
    - 项目管理
    - 分组管理
    - 用户管理

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
