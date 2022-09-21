# PhantomSilhouette

普通に喋る音声を入れると囁き声に変換されます．

## こんな感じになります(音あり)


## 進捗
- [x] PhantomSilhouetteの実装
  - [x] 雑音駆動音声の実装
    - F0を0~1の白色雑音に入れ替え([2] 2.1参照)
  - [x] F1,F2の上方シフトの実装
    - スペクトル包絡を画像的にワープ処理することにより上方シフトを実現([2] 2.2参照)
  - [x] 気息音成分の補填
    - スペクトル包絡の高域部分に正の重みづけ([2] 2.4参照)
  - [x] スペクトル低域抑圧
    - スペクトル包絡の低域部分に負の重みづけ([2] 2.3参照)
- [ ] PhantomSilhouette2の実装
  - [ ] F1,F2帯域の上方シフト量の改良
  - [ ] 高域気息成分の補填量の適応的補正
  - [ ] 低域スペクトルの抑圧対象の拡大

## 参考文献
- [1] Uchida, T. & Morise, M. (2021).  
  A practical method of generating whisper voice: Development of phantom silhouette method and its improvement.  
  Acoustical Science & Technology, 42 (4) 214-217.  
  [https://doi.org/10.1250/ast.42.214](https://doi.org/10.1250/ast.42.214)
- [2] [実用的なささやき声の生成法:Phantom Silhouette方式とその評価](https://jglobal.jst.go.jp/detail?JGLOBAL_ID=201902255241782790)
- [3] [実用的なささやき声の生成法:Phantom Silhouette方式の改良](https://jglobal.jst.go.jp/detail?JGLOBAL_ID=202002252470550660)