<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2024數位聯網智動化競賽</title>
    <link rel="stylesheet" href="all.css">
    <link rel="stylesheet" href="header.css">
    <link rel="stylesheet" href="footer.css">
    <link rel="icon" href="https://pic.pngsucai.com/00/91/31/c65b52a850d8b4f0.webp" type="image/x-icon">
    <!-- AJAX -->
    <script src="https://code.jquery.com/jquery-3.4.1.js"
        integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU=" crossorigin="anonymous"></script>
    <script>let count = 0, race=0, totalrace=0, win=0,lose=0,rate=0</script>
</head>

<body>
    <div class="background-black">
        <div class="hintArea">
            <div class="load-screen">
                <span class='cirlce'></span>
                <span class='load-text'>請稍後...</span>
            </div>
        </div>
    </div>
    <?php
    include ("header.html"); ?>
    <div class="contain">
        <div class="container">
            <div class="stockList_container">
                <?php
                $folderPath = "todayResult/";
                $PerformanceListPath = $folderPath . "Performance_list.json";
                if (file_exists($PerformanceListPath)) {
                    // 讀取策略
                    $strategyfilePath = "Strategy.txt";
                    $strategyFile = fopen($strategyfilePath, "r");
                    $strategy = fread($strategyFile, filesize($strategyfilePath));
                    // 讀取分析資料Json
                    $file = fopen($PerformanceListPath, 'r');
                    $data = fread($file, filesize($PerformanceListPath));
                    $jsonData = json_decode($data);
                    foreach ($jsonData as $item) {
                        echo "<div class='stockList_item'>
                                <div class='item-innerform'>";
                        foreach ($item as $key => $value) {
                            if (str_ends_with($value, "_predict.png")) {
                                echo "<div class = 'item-innerform-imgbox'>";
                                echo "<img class = 'item-innerform-img-predict' src='$value' alt=''><br/>";
                                continue;
                            }
                            if($value === null){
                                echo "<p class='item-baktest-p'>$key ： <sapn style = 'color:gray;font-size:16px;line-height:20px'>無資料</span></p>";
                                continue;
                            }
                            if (str_ends_with($value,".png")){
                                echo"<img class = 'item-innerform-img' src='$value' alt=''><br/>";
                                echo "</div>";
                                continue; 
                            }else if (str_ends_with($key, "標的代號")) {
                                echo "<div class='item-baktest'>";
                                echo "<p class='item-baktest-p'>$key ： $value</p>";
                            } elseif (str_ends_with($key, "期望值") && $value > 0) {
                                echo "<p class='item-baktest-p'><span class='positiveValue'>$key ： $value</span></p>";
                                echo "<script>count++;console.log('紅次數:'+count)</script>";
                            }else if(str_ends_with($key, "總報酬率") && $value > 0){
                                echo "<p class='item-baktest-p'>$key ： $value</p>";
                            }else if(str_ends_with($key, "交易次數")){
                                echo "<p class='item-baktest-p'>$key ： $value</p>";
                                echo "<script>race=$value;totalrace+=race;</script>";
                            }else if(str_ends_with($key, "平均勝率")){
                                echo "<p class='item-baktest-p'>$key ： $value</p>";
                                echo "<script>win+=race*$value;lose+=race*(1-$value)</script>";
                            }else if(str_ends_with($key, "篩選策略")){
                                echo "<p class='item-baktest-p' style = 'width : 98%;padding-top : 25px'>$key ： $strategy</p>";
                            }
                            else {
                                echo "<p class='item-baktest-p'>$key ： $value</p>";
                            }
                        }
                        echo "</div>
                            </div>
                            </div>";
                    }
                    echo"<script>rate=win/totalrace;console.log('總次數:'+totalrace+'\t勝場:'+win+'\t敗場:'+lose+'\t勝率:'+rate);</script>";
                } else {
                    echo "<h1 class= 'welcome'>目前沒有數據唷~<br/>請按右上方開始分析</h1>";
                }
                ?>
            </div>
        </div>
    </div>
    <?php
    include ('footer.html');
    ?>
    <script>
        function startAnalysis() {
            Analysisbtn = document.getElementById("AnalysisBtn");
            openCircle("正在分析 請稍後...")
            $.ajax({
                url: "Analysis_back.php",
                type: "POST",
                data: {},
                success: function (res) {
                    console.log(res);
                    closeCircle(res);
                },
                error: function (err) { 
                    console.log(res);
                    closeCircle(err); 
                },//錯誤訊息
            });
        };
        function updateStockList() {
            updatebtn = document.getElementById("updateBtn");
            openCircle("正在更新中...")
            $.ajax({
                url: "updateStockList.php",
                type: "POST",
                data: {},//length:驗證碼長度、newAccount:新增的帳號名稱
                success: function (res) {
                    console.log(res);
                    // 需顯示寄送完成提示，未完成!
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
            }, 1500);
        }
    </script>
</body>

</html>