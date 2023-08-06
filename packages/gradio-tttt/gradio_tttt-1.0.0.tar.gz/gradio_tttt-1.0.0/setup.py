from distutils.core import setup

setup(
    name='gradio_tttt',  # 对外模块的名字
    version='1.0.0',  # 版本号
    description='测试本地发布模块',  # 描述
    author='zzzz',  # 作者
    author_email='aiteerzhao@gmail.com',
    py_modules=['gradio_tttt.add'],  # 要发布的模块
    # packages=['components', 'themes', 'themes.utils'],  # 要发布的包目录
    # data_files=[]
)