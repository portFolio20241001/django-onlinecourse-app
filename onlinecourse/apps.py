# Djangoのアプリケーション設定を行うためのクラスをインポート
from django.apps import AppConfig  

# アプリケーション設定用のクラスを定義（Djangoは各アプリに対して設定クラスを利用可能）
class OnlinecourseConfig(AppConfig):  
    # アプリケーションの名前を定義（この設定によりDjangoがアプリを識別できる）
    name = 'onlinecourse'  
