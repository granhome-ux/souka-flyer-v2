# ============================================================
# souka-flyer 画像素材 リネーム＆配置スクリプト（商品画像101枚版）
# ============================================================
$sourceDir = ".\_source"
$targetDir = ".\images"

if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
    Write-Host "Created: $targetDir" -ForegroundColor Green
}

$renameMap = @{
    # === ブランド画像（1枚） ===
    "IMG_1745.png" = "mango_taiyo_no_tamago.png"

    # === 果物 スタイルA（5枚） ===
    "IMG_1738.png" = "star_fruit.png"
    "IMG_1739.png" = "lychee.png"
    "IMG_1740.png" = "dragon_fruit.png"
    "IMG_1741.png" = "passion_fruit.png"
    "IMG_1742.png" = "delaware.png"

    # === 果物 スタイルB（34枚） ===
    "IMG_1728.png" = "cherry.png"
    "IMG_1729.png" = "ponkan.png"
    "IMG_1730.png" = "yuzu.png"
    "IMG_1731.png" = "buntan.png"
    "IMG_1732.png" = "iyokan.png"
    "IMG_1733.png" = "nectarine.png"
    "IMG_1734.png" = "guava.png"
    "IMG_1735.png" = "papaya.png"
    "IMG_1736.png" = "kodama_suika.png"
    "IMG_1737.png" = "ao_ume.png"
    "IMG_1743.png" = "plum.png"
    "IMG_1744.png" = "prune.png"
    "IMG_1746.png" = "avocado.png"
    "IMG_1747.png" = "mango.png"
    "IMG_1748.png" = "anzu.png"
    "IMG_1749.png" = "raspberry.png"
    "IMG_1750.png" = "pear_western.png"
    "IMG_1751.png" = "chestnut.png"
    "IMG_1752.png" = "grapefruit.png"
    "IMG_1753.png" = "pomegranate.png"
    "IMG_1754.png" = "lime.png"
    "IMG_1755.png" = "sudachi.png"
    "IMG_1756.png" = "kabosu.png"
    "IMG_1758.png" = "kinkan.png"
    "IMG_1761.png" = "banpeiyu.png"
    "IMG_1762.png" = "dekopon.png"
    "IMG_1763.png" = "kiyomi_orange.png"
    "IMG_1764.png" = "hassaku.png"
    "IMG_1765.png" = "amanatsu.png"
    "IMG_1766.png" = "lemon.png"
    "IMG_1767.png" = "ichijiku.png"
    "IMG_1768.png" = "blueberry.png"
    "IMG_1769.png" = "kaki.png"
    "IMG_1770.png" = "pineapple.png"

    # === 果物 スタイルC（11枚） ===
    "IMG_1771.png" = "kiwi.png"
    "IMG_1772.png" = "muscat.png"
    "IMG_1773.png" = "nashi.png"
    "IMG_1774.png" = "banana.png"
    "IMG_1775.png" = "momo.png"
    "IMG_1776.png" = "kyoho.png"
    "IMG_1777.png" = "mikan.png"
    "IMG_1778.png" = "ringo.png"
    "IMG_1779.png" = "ichigo_red.png"
    "IMG_1780.png" = "ichigo_white.png"
    "IMG_1781.png" = "suika.png"

    # === 野菜 スタイルC（50枚） ===
    "IMG_1782.png" = "yacon.png"
    "IMG_1783.png" = "mekyabetsu.png"
    "IMG_1784.png" = "ooba.png"
    "IMG_1785.png" = "shishito.png"
    "IMG_1786.png" = "tomato_mini.png"
    "IMG_1787.png" = "paprika.png"
    "IMG_1788.png" = "moroheiya.png"
    "IMG_1789.png" = "enoki.png"
    "IMG_1790.png" = "maitake.png"
    "IMG_1791.png" = "eringi.png"
    "IMG_1792.png" = "bunashimeji.png"
    "IMG_1793.png" = "shiitake.png"
    "IMG_1794.png" = "sora_mame.png"
    "IMG_1795.png" = "snap_endo.png"
    "IMG_1796.png" = "sunny_lettuce.png"
    "IMG_1797.png" = "cauliflower.png"
    "IMG_1798.png" = "celery.png"
    "IMG_1799.png" = "nira.png"
    "IMG_1800.png" = "shungiku.png"
    "IMG_1802.png" = "myoga.png"
    "IMG_1803.png" = "asparagus_white.png"
    "IMG_1804.png" = "asparagus.png"
    "IMG_1805.png" = "zucchini.png"
    "IMG_1806.png" = "okra.png"
    "IMG_1807.png" = "edamame.png"
    "IMG_1808.png" = "naga_negi.png"
    "IMG_1809.png" = "shoga.png"
    "IMG_1810.png" = "kabu.png"
    "IMG_1811.png" = "satoimo.png"
    "IMG_1812.png" = "renkon.png"
    "IMG_1813.png" = "gobo.png"
    "IMG_1814.png" = "takenoko.png"
    "IMG_1815.png" = "broccoli.png"
    "IMG_1816.png" = "corn.png"
    "IMG_1817.png" = "kabocha.png"
    "IMG_1818.png" = "piman.png"
    "IMG_1819.png" = "nasu.png"
    "IMG_1820.png" = "kyuri.png"
    "IMG_1821.png" = "ninniku.png"
    "IMG_1822.png" = "nagaimo.png"
    "IMG_1823.png" = "satsumaimo.png"
    "IMG_1824.png" = "jagaimo.png"
    "IMG_1825.png" = "tamanegi.png"
    "IMG_1826.png" = "ninjin.png"
    "IMG_1827.png" = "daikon.png"
    "IMG_1828.png" = "komatsuna.png"
    "IMG_1829.png" = "horenso.png"
    "IMG_1830.png" = "hakusai.png"
    "IMG_1831.png" = "kyabetsu.png"
    "IMG_1832.png" = "tomato.png"
}

$successCount = 0
$missingCount = 0
$missingFiles = @()

foreach ($entry in $renameMap.GetEnumerator()) {
    $src = Join-Path $sourceDir $entry.Key
    $dst = Join-Path $targetDir $entry.Value
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
        $successCount++
        Write-Host "OK  $($entry.Key) -> $($entry.Value)" -ForegroundColor Green
    } else {
        $missingCount++
        $missingFiles += $entry.Key
        Write-Host "NG  $($entry.Key) NOT FOUND" -ForegroundColor Red
    }
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "成功: $successCount / $($renameMap.Count)" -ForegroundColor Green
if ($missingCount -gt 0) {
    Write-Host "失敗: $missingCount" -ForegroundColor Red
    $missingFiles | ForEach-Object { Write-Host "  - $_" }
}
Write-Host "============================================" -ForegroundColor Cyan
