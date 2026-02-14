# Gitの導入

---
## 1. Gitのインストール

### 1. Gitのインストール

PowerShellで以下を実行(開いたディレクトリ(Home)で実行でOK)

```powershell
winget install git.git
```
上手くいかなかった場合は以下を試してみてください

```powershell
winget install --id Git.Git -e --source winget
```

### 2. Gitの初期設定（自分の名前を登録）

Gitは、保存（コミット）したときに「誰の仕業か」を記録します。まず、世界中のGitにあなたを認識させましょう。
PowerShellで以下の2行を実行してください（`"`の中は自分のものに書き換えてください）。

**注意**<br>
*ここでのユーザー名とパスワードをGitHubの登録したものを使用すること！*

```powershell
git config --global user.name "あなたのユーザー名"
git config --global user.email "your-email@example.com"

```

## 2. GitHubとの連携

### 1. SSH鍵を作成する

まずは、あなたのPCの「印鑑」のようなものを作ります。PowerShellで以下を入力してください。

```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"

```

* **Enterを3回押す:** 保存場所やパスフレーズを聞かれますが、最初は空欄のまま（Enterキーのみ）でOKです。
* これで、`C:\Users\(ユーザー名)\.ssh\` フォルダの中に2つのファイルが作られます。
* `id_ed25519`（秘密鍵：**絶対に人に渡さない！**）
* `id_ed25519.pub`（公開鍵：GitHubに渡すもの）



### 2. 公開鍵をコピーする

次に、GitHubに登録するための「公開鍵」の中身を表示させてコピーします。

```powershell
cat ~/.ssh/id_ed25519.pub

```

表示された `ssh-ed25519 AAA...` から始まる長い文字列を、**端から端まで全てコピー**してください。

### 3. GitHubに登録する

1. [GitHubのSSH設定ページ](https://github.com/settings/keys)にアクセスします。
2. **[New SSH key]** ボタンを押します。
3. **Title:** 「My Windows Laptop」など好きな名前を付けます。
4. **Key:** 先ほどコピーした文字列を貼り付けます。
5. **[Add SSH key]** を押して完了です。

### 4. 接続テスト

最後に、正しく設定できたかGitHubに「もしもーし！」と確認の通信を送ります。

```powershell
ssh -T git@github.com

```

* 途中で `Are you sure you want to continue connecting (yes/no/[fingerprint])?` と聞かれたら、**`yes`** と打ってEnter。
* **「Hi (あなたの名前)! You've successfully authenticated...」** と返ってくれば大成功です！

---

### 注意点：SSHを使うときのURL

今後、GitHubからプロジェクトをダウンロード（クローン）するときは、URLの形式に気をつけてください。

* **HTTPSの場合:** `https://github.com/user/repo.git`
* **SSHの場合:** `git@github.com:user/repo.git` **←こちらを使います**

---

### 豆知識：なぜSSH鍵がいいの？

SSH鍵を設定しておくと、`git push` や `git pull` をするたびにユーザー名やパスワードを入力する必要がなくなります。さらに、GitHub CLIが使えないような特殊な環境でも、SSHさえあれば通信できるので汎用性が高いですよ。