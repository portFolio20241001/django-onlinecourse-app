"""
myproject の URL 設定

`urlpatterns` リストは URL をビューにルーティングします。
詳しくは公式ドキュメントを参照してください:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/

【例: 関数ベースビュー (Function views)】
    1. インポートする: from my_app import views
    2. ルーティングを追加: path('', views.home, name='home')

【例: クラスベースビュー (Class-based views)】
    1. インポートする: from other_app.views import Home
    2. ルーティングを追加: path('', Home.as_view(), name='home')

【例: 別の URLconf を含める (Including another URLconf)】
    1. `include()` をインポート: from django.urls import include, path
    2. ルーティングを追加: path('blog/', include('blog.urls'))
"""

# Django 管理サイト（Admin）のモジュールをインポート
from django.contrib import admin

# URL 設定に使用する `path` 関数と `include` 関数をインポート
from django.urls import include, path  

# 静的ファイル (メディアファイル) の設定に必要なモジュールをインポート
from django.conf.urls.static import static  
from django.conf import settings  

# `urlpatterns` はプロジェクトの URL 設定を定義するリスト
urlpatterns = [
    # Django 管理サイト (http://127.0.0.1:8000/admin/) へのルート
    path('admin/', admin.site.urls),  

    # `onlinecourse` アプリの URL 設定をインクルード (http://127.0.0.1:8000/onlinecourse/)
    path('onlinecourse/', include('onlinecourse.urls')),  
] 

# メディアファイル (画像や動画など) のルートを設定
# `settings.MEDIA_URL` にアクセスがあった場合、`settings.MEDIA_ROOT` からファイルを提供する
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
