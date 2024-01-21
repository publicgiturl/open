import json
from tqdm import tqdm
from coco_merge import *


def getbbox(points):
    polygons = np.array(points)
    x,y = polygons[:,0], polygons[:,1]
    bbox = [round(x.min(),2),round(y.min(),2), round(x.max()-x.min(),2),round(y.max()-y.min(),2)]
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return bbox, area

def get_seg(points):
    x = []
    y = []
    for seg_idx, seg in enumerate(points[0]):
        if seg_idx % 2 == 0:
            if str(seg) == '-0.0':
                seg = 0.0
            x.append(seg)
        else:
            if str(seg) == '-0.0':
                seg = 0.0
            y.append(seg)
    seg = np.array([(x, y) for x, y in zip(x, y)])
    return seg

# 3 567 1693 1042
car_1 = [[984.6, 950.97, 984.6, 941.19, 985.83, 932.02, 989.49, 923.45, 997.44, 916.73, 1006.0, 912.45, 1014.56, 907.56, 1023.74, 904.5, 1033.52, 902.05, 1045.14, 902.05, 1057.98, 901.44, 1067.76, 901.44, 1077.55, 901.44, 1087.33, 901.44, 1097.11, 901.44, 1107.51, 901.44, 1117.29, 902.05, 1121.57, 906.33, 1137.47, 914.89, 1152.76, 919.79, 1173.55, 932.02, 1204.12, 939.35, 1216.96, 950.36, 1226.14, 965.03, 1226.75, 976.04, 1224.91, 985.83, 1216.96, 990.72, 1207.18, 991.94, 1198.01, 992.55, 1188.22, 990.11, 1180.28, 995.0, 1171.71, 999.28, 1162.54, 1001.11, 1152.15, 1000.5, 1144.81, 993.77, 1138.08, 985.83, 1128.3, 985.21, 1118.52, 985.21, 1108.73, 985.21]]
car_2 = [[1505.39, 879.74, 1505.39, 875.81, 1505.14, 872.12, 1505.14, 868.19, 1505.39, 864.5, 1505.64, 860.81, 1507.11, 857.13, 1509.32, 853.93, 1512.03, 851.23, 1514.97, 848.77, 1517.68, 846.07, 1520.13, 842.63, 1522.35, 839.44, 1524.8, 836.24, 1527.51, 833.54, 1530.7, 831.08, 1534.39, 829.36, 1538.07, 828.62, 1541.76, 828.38, 1545.45, 828.87, 1549.62, 828.87, 1553.56, 828.87, 1557.24, 829.36, 1561.17, 829.85, 1564.86, 830.1, 1568.55, 830.34, 1572.48, 830.34, 1576.41, 830.34, 1580.34, 830.83, 1584.03, 831.82, 1587.71, 832.31, 1591.15, 835.01, 1593.61, 837.96, 1596.07, 841.4, 1598.53, 844.6, 1600.74, 847.79, 1603.19, 850.74, 1603.44, 854.43, 1602.95, 858.11, 1602.7, 861.8, 1602.95, 865.48, 1603.19, 869.17, 1602.7, 872.86, 1601.72, 876.54, 1600.98, 880.23, 1597.54, 881.95, 1593.36, 881.95, 1590.66, 878.75, 1586.73, 878.51, 1583.04, 879.49, 1580.34, 882.19, 1579.11, 885.88, 1576.65, 889.07, 1572.97, 889.57, 1569.28, 889.32, 1566.33, 886.86, 1562.65, 886.13, 1556.75, 885.88, 1552.57, 885.63, 1548.64, 885.63, 1544.71, 885.63, 1540.78, 885.63, 1536.84, 885.63, 1532.91, 885.63, 1528.74, 885.14, 1524.56, 884.9, 1520.87, 884.65, 1516.94, 884.65, 1512.76, 884.65, 1508.83, 884.65, 1506.37, 884.65]]
car_3 = [[1141.14, 895.94, 1150.92, 893.49, 1160.71, 892.88, 1170.49, 892.88, 1180.28, 892.88, 1189.45, 893.49, 1201.07, 893.49, 1210.85, 893.49, 1223.08, 893.49, 1232.86, 894.1, 1242.03, 896.55, 1251.21, 899.0, 1260.99, 902.05, 1267.82, 907.64, 1272.51, 912.05, 1282.32, 919.02, 1288.44, 922.15, 1300.38, 924.57, 1315.46, 927.98, 1326.42, 930.18, 1332.53, 937.52, 1334.98, 946.69, 1334.98, 956.47, 1331.92, 966.26, 1322.75, 969.32, 1313.58, 969.93, 1303.18, 969.93, 1294.01, 966.87, 1285.45, 971.15, 1276.89, 967.48, 1274.5, 958.7, 1272.8, 954.57, 1270.81, 947.18, 1267.96, 940.92, 1267.25, 939.5, 1256.1, 935.68, 1246.93, 934.46, 1237.14, 929.57, 1228.58, 925.9, 1218.8, 920.4, 1211.46, 914.28, 1204.73, 907.56, 1196.79, 902.05]]
car_4 = [[1106.9, 899.0, 1116.07, 898.38, 1125.24, 897.77, 1135.64, 897.77, 1144.81, 897.16, 1154.59, 897.16, 1163.77, 897.77, 1172.94, 898.38, 1182.11, 899.61, 1191.28, 900.83, 1200.45, 903.89, 1207.79, 910.0, 1215.74, 915.51, 1222.47, 922.23, 1231.03, 925.9, 1238.98, 930.79, 1266.49, 938.74, 1270.77, 947.3, 1273.22, 956.47, 1274.44, 965.65, 1272.0, 974.82, 1263.44, 979.1, 1254.26, 979.71, 1245.09, 979.1, 1235.92, 978.49, 1227.36, 974.82, 1226.7, 965.0, 1223.1, 957.1, 1218.2, 948.5, 1209.63, 944.24, 1200.45, 941.8, 1191.28, 939.35, 1182.11, 936.3, 1172.94, 932.63, 1164.38, 928.35, 1155.82, 924.68, 1147.26, 920.4, 1138.69, 916.12, 1130.13, 911.84, 1121.57, 908.17]]
car_5 = [[1513.25, 975.82, 1516.45, 971.64, 1518.41, 968.45, 1520.38, 965.25, 1522.35, 961.81, 1524.56, 958.62, 1527.02, 955.42, 1529.47, 952.23, 1532.42, 949.28, 1535.12, 946.58, 1538.07, 943.38, 1540.53, 940.43, 1542.99, 937.49, 1545.69, 934.29, 1549.38, 931.59, 1552.57, 929.62, 1556.01, 927.9, 1559.45, 926.43, 1563.14, 925.44, 1567.56, 924.71, 1571.99, 923.97, 1575.67, 923.48, 1579.6, 922.74, 1583.78, 922.0, 1587.47, 921.27, 1591.15, 920.78, 1594.84, 920.28, 1599.51, 920.28, 1603.19, 920.04, 1606.88, 919.55, 1610.57, 919.06, 1614.5, 918.81, 1618.43, 918.81, 1622.61, 918.81, 1626.54, 918.81, 1630.47, 918.81, 1634.16, 919.3, 1638.34, 919.79, 1642.02, 920.53, 1645.71, 920.78, 1649.64, 921.27, 1653.57, 921.51, 1657.5, 922.0, 1662.17, 922.5, 1666.35, 923.23, 1670.77, 924.22, 1674.7, 924.95, 1678.64, 925.44, 1682.32, 926.92, 1684.53, 930.36, 1685.76, 934.05, 1686.5, 937.98, 1687.48, 941.66, 1688.22, 945.35, 1688.96, 949.04, 1689.45, 952.72, 1689.94, 956.41, 1690.43, 960.09, 1690.68, 964.03, 1691.17, 967.71, 1691.17, 971.64, 1691.42, 975.33, 1691.66, 979.02, 1691.66, 983.19, 1691.66, 987.13, 1691.91, 990.81, 1691.91, 994.74, 1691.66, 998.43, 1690.43, 1002.12, 1687.48, 1004.82, 1684.04, 1006.78, 1680.36, 1008.01, 1676.67, 1009.0, 1672.98, 1009.49, 1669.3, 1010.22, 1665.61, 1010.47, 1661.93, 1011.45, 1658.24, 1011.94, 1653.82, 1013.17, 1649.89, 1013.66, 1646.2, 1014.4, 1642.27, 1015.14, 1638.34, 1016.12, 1637.11, 1017.35, 1633.17, 1017.84, 1629.24, 1018.83, 1625.31, 1020.05, 1621.38, 1021.04, 1617.45, 1021.53, 1613.52, 1022.51, 1609.58, 1023.49, 1605.65, 1024.48, 1601.72, 1025.21, 1597.79, 1026.2, 1594.1, 1027.18, 1590.17, 1027.43, 1585.99, 1027.18, 1582.06, 1026.69, 1578.13, 1026.69, 1573.95, 1026.93, 1569.77, 1026.93, 1565.6, 1026.93, 1561.42, 1027.18, 1557.24, 1027.43, 1553.56, 1027.67, 1549.62, 1027.92, 1545.45, 1027.92, 1541.02, 1027.92, 1536.84, 1027.43, 1533.16, 1026.93, 1528.74, 1026.2, 1527.51, 1022.02, 1528.24, 1018.33, 1529.23, 1014.65, 1530.21, 1009.98, 1530.7, 1005.8, 1531.19, 1001.87, 1531.19, 997.94, 1529.96, 994.01, 1527.51, 990.32, 1525.05, 987.13, 1522.35, 983.68, 1519.89, 980.49, 1516.94, 978.28]]

arrow_1 = [[3519.46, 1358.45, 3517.63, 1440.61, 3751.34, 1457.04, 3749.52, 1378.53]]
arrow_2 = [[701.7, 1424.8, 784.55, 1400.63, 825.72, 1401.36, 881.41, 1387.42, 1013.49, 1342.66, 1002.56, 1336.79, 863.87, 1382.28, 843.99, 1385.95, 827.11, 1387.42, 875.61, 1369.81, 755.2, 1387.42]]
arrow_3 = [[1168.66, 1247.98, 1369.5, 1288.15, 1517.4, 1227.9, 1327.51, 1191.38]]
arrow_4 = [[1668.24, 1626.41, 1473.05, 1588.99, 1673.37, 1484.79, 1837.0, 1523.68]]
arrow_5 = [[332.55, 1297.17, 426.5, 1259.0, 404.46, 1257.54, 474.97, 1216.45, 459.49, 1214.98, 389.78, 1256.07, 364.91, 1256.81]]
arrow_6 =[[2394.7, 839.5, 2485.87, 845.6, 2508.23, 829.14, 2417.8, 823.49]]
arrow_7 = [[842.09, 1634.52, 1066.69, 1571.34, 1049.89, 1563.3, 1274.29, 1475.3, 1260.42, 1469.45, 1035.11, 1558.19, 1009.54, 1554.54]]
arrow_8 = [[3072.24, 1314.81, 3043.74, 1381.41, 3259.3, 1405.73, 3286.74, 1343.41]]
arrow_9 = [[2611.7, 1335.0, 2818.43, 1359.44, 2847.8, 1295.8, 2675.34, 1275.05]]
arrow_10 = [[894.7, 1928.7, 1170.49, 1826.0, 1146.03, 1816.21, 1406.52, 1691.47, 1388.79, 1684.75, 1124.02, 1813.16, 1092.22, 1806.43, 1004.78, 1861.46]]
arrow_11 = [[1338.46, 1395.88, 1499.14, 1432.39, 1647.03, 1350.23, 1510.09, 1317.36]]
arrow_12 = [[2747.8, 857.9, 2847.1, 865.51, 2855.95, 845.36, 2757.16, 840.93]]
arrow_13 = [[2575.05, 850.5, 2663.73, 856.44, 2679.91, 838.82, 2584.68, 834.93]]

building_1 =[[2463.8, 487.3, 2487.17, 490.23, 2510.53, 502.67, 2530.32, 503.52, 2536.22, 491.42, 2551.55, 488.78, 2559.53, 483.48, 2658.94, 468.06, 2704.84, 463.9, 2705.82, 488.02, 2801.92, 490.53, 2840.6, 492.69, 2864.21, 494.81, 2862.09, 528.66, 2915.97, 536.47, 2957.12, 545.05, 3041.58, 562.46, 3102.52, 575.41, 3166.51, 590.95, 3241.46, 613.29, 3333.44, 645.48, 3385.11, 665.65, 3438.19, 690.45, 3466.52, 706.37, 3499.81, 723.44, 3523.04, 739.36, 3548.73, 756.48, 3582.95, 782.17, 3630.34, 825.74, 3839.56, 846.03, 3840.0, 835.19, 3840.0, 458.72, 3836.0, 456.64, 3836.42, 440.5, 3814.34, 425.22, 3803.64, 420.76, 3772.98, 439.02, 3770.35, 449.63, 3753.23, 447.89, 3757.65, 415.45, 3752.04, 414.86, 3720.2, 415.45, 3733.15, 320.71, 3731.07, 318.93, 3711.62, 308.02, 3664.14, 302.11, 3665.59, 281.18, 3639.35, 266.44, 3624.31, 264.96, 3595.44, 282.96, 3594.84, 291.8, 3551.49, 287.68, 3519.94, 305.94, 3511.95, 364.92, 3508.43, 364.92, 3509.02, 357.57, 3499.3, 350.48, 3498.71, 344.58, 3476.92, 329.33, 3448.47, 327.21, 3448.73, 307.85, 3429.83, 296.04, 3413.57, 294.81, 3388.47, 308.4, 3387.62, 315.45, 3354.88, 315.74, 3355.18, 305.72, 3327.75, 286.87, 3328.04, 275.96, 3302.39, 257.36, 3290.59, 258.25, 3259.04, 269.16, 3255.22, 290.99, 3246.64, 288.36, 3238.1, 293.37, 3216.28, 302.2, 3213.9, 305.13, 3207.15, 368.82, 3199.46, 370.31, 3201.25, 352.05, 3189.14, 343.18, 3171.44, 341.99, 3173.81, 320.76, 3171.44, 317.19, 3168.38, 314.51, 3165.92, 312.26, 3163.07, 310.22, 3159.8, 308.4, 3156.91, 306.74, 3154.24, 305.09, 3151.39, 303.47, 3148.51, 301.6, 3145.87, 299.99, 3143.2, 297.95, 3140.35, 295.87, 3137.89, 293.83, 3135.21, 292.01, 3132.75, 289.97, 3130.29, 287.89, 3127.83, 285.64, 3125.19, 283.39, 3122.52, 281.35, 3119.84, 279.31, 3117.21, 277.65, 3114.54, 276.04, 3111.86, 273.96, 3109.4, 271.92, 3106.93, 269.67, 3104.3, 268.06, 3101.63, 266.4, 3098.74, 265.17, 3095.68, 264.58, 3091.82, 264.75, 3088.5, 264.96, 3084.85, 264.96, 3081.37, 265.17, 3078.06, 265.38, 3075.0, 265.6, 3071.94, 265.81, 3068.67, 265.98, 3065.19, 266.19, 3064.17, 264.62, 3079.76, 130.9, 3087.19, 57.27, 3073.73, 39.22, 3065.96, 38.5, 3000.14, 33.57, 3004.25, 0.0, 2946.2, 0.0, 2942.34, 28.56, 2863.96, 21.64, 2795.89, 16.5, 2803.12, 0.0, 2743.04, 0.0, 2740.9, 10.77, 2664.42, 5.33, 2651.59, 38.97, 2645.48, 103.77, 2592.27, 99.52, 2580.04, 129.46, 2568.54, 234.3, 2490.4, 229.2, 2482.33, 250.01, 2468.32, 385.05, 2463.33, 469.6]]
building_2 = [[1.46, 242.09, 24.17, 244.45, 73.12, 250.05, 110.57, 254.18, 170.43, 260.38, 230.59, 266.57, 291.04, 273.06, 357.69, 280.72, 536.1, 298.71, 709.49, 318.47, 848.97, 334.1, 974.3, 345.6, 1118.5, 360.34, 1216.4, 370.07, 1422.53, 392.19, 1527.8, 401.92, 1530.16, 401.92, 1536.06, 412.24, 1541.07, 413.72, 1539.89, 449.99, 1598.28, 455.3, 1705.91, 403.99, 1703.56, 401.33, 1700.9, 399.86, 1697.66, 398.68, 1694.41, 398.09, 1691.46, 397.2, 1690.88, 393.96, 1690.88, 388.95, 1691.46, 384.52, 1691.46, 381.28, 1691.46, 377.74, 1691.76, 374.5, 1692.35, 371.25, 1692.35, 368.3, 1692.64, 365.36, 1692.64, 361.82, 1692.94, 358.57, 1692.94, 355.33, 1692.94, 351.79, 1693.53, 348.84, 1694.41, 339.11, 1696.77, 339.7, 1699.13, 340.29, 1701.2, 341.17, 1703.26, 341.17, 1705.62, 341.76, 1707.68, 342.06, 1709.75, 342.35, 1710.93, 340.29, 1711.22, 337.93, 1717.42, 248.58, 1714.17, 246.22, 1710.63, 245.63, 1706.8, 244.45, 1703.26, 243.86, 1699.43, 243.27, 1697.36, 240.03, 1695.89, 236.78, 1695.59, 232.66, 1695.59, 228.82, 1695.59, 224.99, 1692.64, 222.33, 1690.88, 219.09, 1689.99, 215.26, 1693.53, 213.78, 1697.95, 212.9, 1701.49, 212.01, 1703.56, 215.26, 1703.85, 218.5, 1756.05, 168.37, 1762.24, 103.79, 1789.66, 109.1, 1795.27, 109.98, 1799.1, 111.16, 1802.64, 111.75, 1805.88, 112.34, 1810.3, 113.23, 1815.02, 113.82, 1820.04, 114.7, 1824.46, 115.88, 1828.0, 116.47, 1832.72, 117.94, 1838.02, 119.12, 1840.97, 119.42, 1843.92, 120.6, 1849.23, 121.48, 1852.77, 122.66, 1856.31, 123.25, 1861.62, 124.43, 1865.74, 125.32, 1871.05, 126.5, 1874.89, 127.68, 1879.01, 128.56, 1882.26, 129.15, 1885.5, 130.62, 1889.04, 131.8, 1891.69, 132.98, 1893.17, 133.28, 1919.41, 146.84, 1917.94, 166.6, 1912.63, 168.37, 1908.5, 168.08, 1909.68, 171.32, 1909.98, 174.27, 2198.97, 192.85, 2200.44, 194.03, 2205.16, 179.28, 2206.34, 172.79, 2206.93, 166.9, 2207.52, 161.0, 2207.52, 154.81, 2207.52, 148.61, 2207.81, 142.72, 2208.7, 136.82, 2209.29, 131.51, 2209.88, 126.2, 2209.88, 120.3, 2210.47, 115.0, 2210.76, 109.1, 2211.35, 103.79, 2216.95, 102.61, 2222.85, 102.61, 2227.28, 105.26, 2233.76, 105.26, 2238.78, 108.51, 2244.08, 109.1, 2249.39, 109.69, 2253.23, 113.52, 2252.93, 119.12, 2251.46, 124.43, 2251.46, 130.33, 2245.26, 188.42, 2248.21, 200.51, 2317.81, 204.05, 2324.59, 294.29, 2356.14, 305.49, 2367.35, 324.07, 2385.04, 331.44, 2388.87, 332.62, 2401.26, 356.21, 2400.08, 367.12, 2397.43, 370.37, 2394.77, 371.25, 2393.59, 379.8, 2384.45, 475.94, 2393.89, 488.32, 2380.62, 599.5, 2389.76, 601.56, 2389.17, 613.36, 2390.64, 623.09, 2390.94, 629.57, 2388.58, 636.65, 2384.16, 639.01, 2383.57, 643.73, 2383.57, 648.45, 2384.16, 653.46, 2384.16, 658.18, 2384.16, 663.19, 2384.45, 667.91, 2385.04, 672.63, 2385.34, 677.05, 2385.04, 681.47, 2384.45, 685.9, 2384.16, 690.32, 2383.86, 694.74, 2383.86, 700.35, 2383.86, 705.66, 2383.86, 711.26, 2383.57, 715.68, 2382.98, 720.69, 2382.39, 725.12, 2381.21, 729.84, 2379.44, 734.26, 2377.67, 739.27, 2374.42, 742.52, 2370.59, 745.76, 2365.87, 748.71, 2361.74, 751.95, 2358.21, 754.9, 2354.37, 757.56, 2352.31, 776.72, 2304.54, 796.78, 2226.39, 826.26, 2120.23, 859.88, 1982.52, 900.58, 1781.11, 956.6, 1692.94, 979.31, 1692.64, 974.89, 1692.35, 970.46, 1690.88, 963.98, 1690.88, 959.26, 1690.88, 953.95, 1690.29, 948.94, 1689.4, 944.22, 1688.22, 939.5, 1686.75, 934.78, 1684.98, 930.65, 1682.91, 926.53, 1677.31, 924.76, 1672.59, 923.87, 1668.17, 922.69, 1663.16, 921.51, 1657.85, 920.92, 1651.95, 920.63, 1646.94, 920.63, 1642.22, 920.63, 1637.21, 920.63, 1631.9, 920.33, 1627.47, 920.04, 1623.05, 919.45, 1621.58, 914.14, 1620.69, 909.72, 1619.22, 903.82, 1618.04, 898.51, 1626.29, 787.63, 1652.54, 780.56, 1655.78, 731.02, 1642.81, 728.36, 1642.51, 721.28, 1642.51, 715.68, 1645.17, 711.26, 1649.59, 709.19, 1654.01, 706.25, 1667.28, 705.36, 1670.53, 700.64, 1671.41, 696.22, 1676.13, 695.04, 1679.08, 690.91, 1682.32, 686.19, 1683.5, 680.3, 1683.21, 676.76, 1589.73, 671.74, 1191.93, 641.08, 215.55, 570.6, 0.0, 559.68, 0.0, 277.88]]

lane_1 =[[3230.04, 1925.21, 3297.66, 1751.92, 3375.85, 1556.44, 3402.27, 1458.17, 3427.63, 1336.66, 3433.97, 1262.7, 3434.81, 1184.93, 3435.55, 1138.86, 3431.96, 1081.91, 3429.53, 1045.45, 3424.25, 1000.86, 3418.23, 972.97, 3407.76, 935.98, 3399.52, 913.79, 3388.85, 882.84, 3380.29, 861.07, 3371.2, 861.39, 3379.45, 883.15, 3390.33, 915.27, 3396.88, 935.67, 3407.45, 974.87, 3411.04, 1001.39, 3416.64, 1045.98, 3419.28, 1082.86, 3421.08, 1138.86, 3419.28, 1184.61, 3417.06, 1265.65, 3407.24, 1334.34, 3379.45, 1456.8, 3352.5, 1550.31, 3271.04, 1741.99, 3198.02, 1917.18]]
lane_2 =[[923.04, 1482.67, 1344.81, 1336.6, 1615.77, 1236.17, 1766.77, 1177.38, 1940.41, 1109.46, 2031.52, 1073.49, 2162.44, 1026.93, 2231.64, 996.8, 2324.21, 956.82, 2378.8, 929.98, 2519.76, 856.76, 2555.0, 829.74, 2598.45, 799.98, 2613.79, 788.47, 2645.56, 765.47, 2658.89, 753.23, 2679.52, 735.52, 2686.46, 725.3, 2701.07, 710.14, 2707.09, 700.83, 2714.03, 688.23, 2717.5, 680.2, 2718.96, 669.61, 2719.33, 661.39, 2719.33, 651.53, 2717.5, 642.95, 2714.76, 635.1, 2712.39, 628.34, 2708.01, 628.53, 2710.38, 635.65, 2713.12, 643.68, 2715.13, 651.35, 2714.58, 660.84, 2713.67, 668.7, 2711.47, 679.83, 2708.92, 687.68, 2703.08, 699.37, 2697.05, 708.86, 2681.9, 724.38, 2672.95, 734.43, 2652.13, 753.42, 2639.35, 764.37, 2607.77, 787.01, 2592.25, 798.33, 2547.88, 828.64, 2514.28, 853.11, 2371.68, 927.79, 2315.99, 954.26, 2222.33, 994.61, 2153.31, 1023.28, 2020.93, 1071.85, 1930.92, 1107.63, 1755.82, 1175.56, 1604.09, 1232.16, 1327.47, 1326.92, 912.27, 1465.69]]
lane_3 =[[260.25, 2066.95, 740.45, 1856.97, 1277.26, 1617.78, 1507.32, 1513.71, 1799.45, 1371.29, 1952.1, 1297.34, 2143.27, 1204.4, 2236.38, 1153.65, 2355.8, 1089.19, 2418.97, 1053.04, 2502.6, 1005.57, 2547.88, 977.08, 2612.2, 936.0, 2639.48, 915.59, 2681.5, 879.71, 2703.9, 860.8, 2738.31, 826.09, 2746.9, 815.86, 2779.03, 786.46, 2791.45, 770.03, 2806.42, 751.77, 2812.81, 739.36, 2821.21, 724.93, 2825.04, 714.89, 2829.97, 701.93, 2831.43, 693.34, 2831.25, 678.92, 2829.43, 672.53, 2825.04, 660.48, 2822.3, 654.45, 2815.0, 640.94, 2812.63, 635.28, 2805.51, 627.61, 2800.76, 622.68, 2796.01, 622.68, 2801.12, 629.07, 2808.43, 638.93, 2811.71, 645.87, 2817.37, 654.45, 2819.75, 662.12, 2824.13, 672.53, 2825.59, 678.74, 2824.31, 692.25, 2823.77, 700.28, 2818.84, 713.43, 2815.0, 724.38, 2806.42, 739.17, 2798.39, 751.77, 2785.42, 770.03, 2772.46, 785.37, 2738.13, 819.69, 2694.8, 861.0, 2675.1, 879.0, 2632.9, 913.5, 2602.9, 934.9, 2537.1, 976.9, 2488.72, 1005.2, 2408.93, 1050.48, 2341.37, 1086.27, 2225.06, 1149.63, 2127.2, 1199.66, 1937.49, 1293.32, 1782.66, 1367.27, 1493.62, 1506.04, 1259.0, 1608.65, 722.19, 1842.36, 238.34, 2055.99]]
lane_4 =[[3186.97, 791.91, 3189.93, 806.92, 3186.77, 836.81, 3186.67, 846.71, 3183.13, 876.56, 3181.01, 896.95, 3173.79, 932.19, 3169.97, 955.55, 3158.08, 993.76, 3149.16, 1021.37, 3125.81, 1076.99, 3112.64, 1109.27, 3076.98, 1169.99, 3037.06, 1228.59, 2973.79, 1316.49, 2916.89, 1390.38, 2806.06, 1521.59, 2710.94, 1636.67, 2495.22, 1855.78, 2296.92, 2049.84, 2271.44, 2041.77, 2468.47, 1848.99, 2683.76, 1625.2, 2783.55, 1514.37, 2898.63, 1384.43, 2956.38, 1310.97, 3023.47, 1222.64, 3060.84, 1167.44, 3096.93, 1105.44, 3115.19, 1069.77, 3139.4, 1018.39, 3146.62, 990.37, 3158.93, 952.15, 3162.75, 930.49, 3169.55, 897.8, 3171.97, 875.71, 3177.47, 846.01, 3177.47, 835.41, 3181.27, 806.41, 3178.89, 791.21]]

file_list = [car_1, car_2, car_3, car_4, car_5, arrow_1, arrow_2, arrow_3, arrow_4, arrow_5, arrow_6, arrow_7, arrow_8, arrow_9, arrow_10, arrow_11, arrow_12,arrow_13,
             building_1, building_2, lane_1, lane_2, lane_3, lane_4]

new_ann = []
for img_id in range(1,330):
    for idx, ind_file in enumerate(file_list):
        if idx < 5:
            cls = 4
        elif idx < 18:
            cls = 7
        elif idx < 20:
            cls = 1
        else:
            cls = 6
        seg = get_seg(ind_file)
        bbox, area = getbbox(seg)
        new_ann.append(dict(id=0,
                            image_id=img_id,
                            category_id=cls,
                            segmentation=ind_file,
                            area=area,
                            bbox=bbox,
                            iscrowd=0,
                            attributes={
                                "occluded": False
                            }
                            ))
with open('D:/download/test2/annotations/instances_default.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    for obj_id, ann in enumerate(tqdm(json_data['annotations'])):
        new_ann.append(ann)


        # x = []
        # y = []
        # for seg_idx, seg in enumerate(ann['segmentation'][0]):
        #     if seg_idx % 2 == 0:
        #         x.append(seg)
        #     else:
        #         y.append(seg)
        # if ann['category_id'] in [7]:
        #     print(ann['segmentation'])
                # continue
#         else:
#             if ann['category_id'] in [1, 6, 7]:
#                 continue
#             else:
#                 new_ann.append(ann)
#
for idx, ann in enumerate(new_ann):
    ann['id']= idx+1
#
new_json = dict(
    info=json_data['info'],
    licenses=json_data['licenses'],
    categories=json_data['categories'],
    images=json_data['images'],
    annotations=new_ann
)


with open(f'D:/download/annotations/instances_default_coco.json', 'w', encoding='utf-8') as new_j:
    json.dump(new_json, new_j, ensure_ascii=False, indent=2, cls=ConvertEncoder)

# import cv2
#
# isDragging = False
# x0, y0, w, h = -1, -1, -1, -1
# blue, red = (255, 0, 0), (0, 0, 255)
#
#
# def onMouse(event, x, y, flags, param):
#     global isDragging, x0, y0, img
#     if event == cv2.EVENT_LBUTTONDOWN:
#         isDragging = True
#         x0 = x
#         y0 = y
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if isDragging:
#             img_draw = img.copy()
#             cv2.rectangle(img_draw, (x0, y0), (x, y), blue, 2)
#             cv2.imshow('img', img_draw)
#             print(x0, y0, x, y)
#     elif event == cv2.EVENT_LBUTTONUP:
#         if isDragging:
#             isDragging = False
#             w = x - x0
#             h = y - y0
#             if w > 0 and h > 0:
#                 img_draw = img.copy()
#                 cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2)
#                 cv2.imshow('img', img_draw)
#                 roi = img[y0:y0 + h, x0:x0 + w]
#                 cv2.imshow('cropped', roi)
#                 cv2.moveWindow('cropped', 0, 0)
#                 cv2.imwrite('./cropped.png', roi)
#             else:
#                 cv2.imshow('img', img)
#                 print('drag should start from left-top side')
#
#
# img = cv2.imread('D:/frame_000002.PNG')
# cv2.imshow('img', img)
# cv2.setMouseCallback('img', onMouse)
# cv2.waitKey()
# cv2.destroyAllWindows()