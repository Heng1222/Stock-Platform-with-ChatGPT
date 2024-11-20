<!DOCTYPE html>
<html >

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2024數位聯網智動化競賽</title>
    <link rel="stylesheet" href="all.css">
    <link rel="stylesheet" href="header.css">
    <link rel="stylesheet" href="footer.css">
    <link rel="icon" href="https://pic.pngsucai.com/00/91/31/c65b52a850d8b4f0.webp" type="image/x-icon">
    <!-- AJAX -->
    <script src="https://code.jquery.com/jquery-3.4.1.js"
        integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU=" crossorigin="anonymous"></script>
    <script>let count = 0, race = 0, totalrace = 0, win = 0, lose = 0, rate = 0</script>
</head>

<body>
    <div class="background-black">
        <div class="hintArea">
            <div class="load-screen">
                <span class='cirlce'></span>
                <span class='load-text'>正在產生策略</span>
                <div class="load-hint-container">
                    <p class='load-hintTopic'>策略方式</p>
                    <p class='load-hint'>基於過去10天股價最高點呈現連續上升趨勢，並當日收盤價高於開盤價，表示市場強勢。透過觀察最高價趨勢，判斷股價可能持續上漲，因此選擇進場。</p>
                </div>
            </div>
        </div>
    </div>
    <?php
    include ("header.html"); ?>
    <div class="contain"
        style="display:flex; justify-content: end;flex-direction: column;padding-bottom:10px;position:relative">
        <h1 class="asking-welcome">歡迎來到台股訊號偵測系統</h1>
        <div class="container asking-page">
            <h1 class="asking-hint">請輸入您想設定的篩選條件，系統將根據您的需求針對股票清單進行分析</h1>
            <form class="asking-form" action="" method="post">
                <input class="asking-userinput" type="text" name="userInput" id="" placeholder="今日KD指標的K和D皆低於20且出現黃金交叉，短期MA高於長期MA，交易量上升">
                <input class="asking-submit" type="submit" value="傳送">
            </form>
        </div>
    </div>
    <?php
    // include ('footer.html');
    // ?>
    <script>
        $(".asking-submit").click(function (evt) {
            evt.preventDefault()
            openCircle("正在生成進場策略")
            console.log("ajax送出")
            getStrategy();
        })
        function getStrategy() {
            var datas = $(".asking-userinput").val()
            console.log(datas);
            $.ajax({
                url: "askingBack.php",
                method: "post",
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                data: {
                    "userInput":datas,
                },
                success: function (res) {
                    console.log('Strategy result:', res);
                    getExplanation(res);
                },
                error:function(res){
                    closeCircle("出錯了")
                }
            });
        }
        function getExplanation(res){
            $.ajax({
                url: "askingBack.php",
                type:"POST",
                contentType: "application/x-www-form-urlencoded;charset='utf-8'",
                data: {
                    "strategy":res,
                },
                success: function (exp) {
                    console.log('Explanation result3:', exp);
                    openCircle("進場策略已生成！")
                    openCircle_explanation(exp);
                    // Execute(res);
                },
                error:function(res){
                    closeCircle("出錯了")
                }
            });
        }
        function Execute(strategy){
            $.ajax({
                url: "askingBack.php",
                method: "post",
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                data: {
                    "execution":strategy,
                },
                success: function (finalres) {
                    finalres = finalres;
                    console.log('Execute result:',finalres);
                    closeCircle("分析完成!");
                },
                error:function(res){
                    closeCircle("出錯了")
                }
            });
        }
    </script>
    <script>
        function updateStockList() {
            updatebtn = document.getElementById("updateBtn");
            openCircle("正在更新中...")
            $.ajax({
                url: "updateStockList.php",
                type: "POST",
                data: {},//length:驗證碼長度、newAccount:新增的帳號名稱
                success: function (res) {
                    console.log(res);
                    closeCircle(res);
                },
                error: function (err) {
                    closeCircle(err);
                    console.log(res);
                },//錯誤訊息
            });
        };
    </script>
    <script>
        function openCircle_explanation(exp){
            const hintContainer = document.querySelector(".load-hint-container")
            const hintTopic = document.querySelector(".load-hintTopic");
            const hint =document.querySelector(".load-hint");
            hint.innerHTML = exp;
            hintContainer.style.display = "block";
            hintTopic.style.display = "block";
            hint.style.display = "block";

        }
        function openCircle(message) {
            const background = document.querySelector(".background-black");
            const hintArea = document.querySelector(".hintArea");
            const hintText = document.querySelector(".load-text");
            hintText.innerHTML = message;
            background.style.height = screen.height + "px";
            background.style.display = "block";
            hintArea.style.display = "block";
        }
        function closeCircle(message) {
            const background = document.querySelector(".background-black");
            const hintArea = document.querySelector(".hintArea");
            const hintText = document.querySelector(".load-text");
            hintText.innerHTML = message;
            setTimeout(function () {
                background.style.display = "none";
                hintArea.style.display = "none";
                document.location.href = "showing.php";
            }, 1500);
        }
    </script>
</body>

</html>