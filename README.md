# ComputerVision_FinalProject
##  高等電腦視覺Final project
### project1
作法說明
1.	將輸入圖像轉成灰階圖
Project1以python進行編譯，圖片輸入後，先進行雙邊濾波轉成灰階圖，最後再resize。原圖像在轉成灰階圖的時候會有一些噪聲無法被濾除，導致影響後面IoU的效果，因此我以高斯濾波、均值濾波、中值濾波及雙邊濾波四種濾波器進行過濾，經測試結果發現在雙邊濾波上的效果最好，因為雙邊濾波在降噪上有顯著的效果，它能保持邊界清晰的情況下有效的去除噪聲，但與其他濾波器相比，操作速度较慢，所以在執行時間上，相對於使用其他濾波器來得長。	 
2.	處理點膠部分
透過點膠後減掉點膠前，可取得點膠部分，接著使用高斯濾波，並將圖像進行二值化，二值化中使用THRESH_BINARY（二進制閾值化），後續將與groundtruth進行IoU計算。  
3.	計算IoU、執行時間
最後利用二值圖與groundtruth進行IoU，這部分我是以邏輯閘and（交集）與or（聯集）進行運算，接著計算輸出的and與or圖的白色區域面積，將這兩個值進行相除就可以得到最終的IoU。
4.	結論
從結果看來，圖一到圖四的IoU效果都還不錯，都保持著80%以上的準確率，但圖五與圖六因為有過度曝光的問題，IoU效果相對於來說較低，圖七因為點膠前後光影變化較明顯，在影像處理上較不容易，IoU的效果也最低。在執行過程中使用了雙邊濾波，所以時間上也相對於使用其他濾波器的執行時間來的長。
-----
### Project2
作法說明
分類點膠後是good還是bad採用的是Pytorch之核心庫支援，並以python進行編譯，以進行深度學習之分類問題，利用老師所提供之資料集進行分類，挑出點交good與bad各58張。由於與自己所設計的網路架構，訓練效果非常不理想，因此考慮採用ResNet進行訓練，ResNet在2015年被提出，在ImageNet比賽classification任務上獲得第一名，因此選擇ResNet101作為此分類的網路模型。 
在影像分類中，卷積神經網路最前面幾層用於辨識影像最基本的特徵，像是物體的紋理、輪廓、顏色等等，較後面的階層才是提取影像重要特徵的關鍵，因此保留CNN底層權重，僅針對後面階層與新的分類器進行訓練即可，一來可套用最好的權重進行學習，二來可以節省訓練時間。基於上述原因採用遷移學習，把已經訓練好的模型和權重直接納入到新的資料集當中進行訓練，只改變之前模型的分類器（全連線層和softmax），將分類輸出成2類，透過逐步解凍的技術，解凍'layer4.0.conv1.weight'後的階層，使模型訓練的效果達到最好。
####    逐步解凍步驟如下
1.凍結預訓練網路的卷積層權重
2.將舊的全連線層，換上新的欲輸出種類個數的全連線層與分類器
3.解凍部分頂部的卷積層，保留底部卷積神經網路的權重
4.對解凍的卷積層與全連線層進行訓練，得到新的權重
以25張bad張圖像進行測試，其ResNet101測試結果以混淆矩陣呈現如下，其測試準確率達72%。
結論
在資料預處理的過程中，以resize進行預處理，在訓練的過程中可能有過度擬合的問題發生，圖像的預處理與調整參數上或許還可以調整更好，以提升訓練成效。




