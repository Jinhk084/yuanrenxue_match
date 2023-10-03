import java.util.ArrayList;

public class Match01 {

    public static String getSign(int page, long timeStamp) {
        StringBuilder sb = new StringBuilder();
        sb.append("page=");
        sb.append(page);
        sb.append(timeStamp);
        String params = sb.toString();
        String result = new Sign().sign(params.getBytes());
        // System.out.println(result); // 正确答案: adfd50c4334f457511f41c3eed3193dd
        return result;
    }
}


class Sign {
    private static final int A = 1732584193;
    private static final int B = -271733879;
    private static final int C = -1732584194;
    private static final int D = 271733878;

    private static int f(int i, int i2, int i3) {
        return ((~i) & i3) | (i2 & i);
    }

    private static int ff(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + f(i2, i3, i4) + i5, i6);
    }

    private static int g(int i, int i2, int i3) {
        return (i & i3) | (i & i2) | (i2 & i3);
    }

    private static int gg(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + g(i2, i3, i4) + i5 + 1518565785, i6);
    }

    private static int h(int i, int i2, int i3) {
        return (i ^ i2) ^ i3;
    }

    private static int hh(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + h(i2, i3, i4) + i5 + 1859775393, i6);
    }

    private ArrayList<Integer> padding(byte[] bArr) {
        long length = bArr.length * 8; // 将原本的 int 数据类型改为long
        ArrayList<Integer> arrayList = new ArrayList<>();
        for (byte b : bArr) {
            arrayList.add(Integer.valueOf(b));
        }
        arrayList.add(128);
        while (((arrayList.size() * 8) + 64) % 512 != 0) {
            arrayList.add(0);
        }
        for (int i = 0; i < 8; i++) {
            arrayList.add(Integer.valueOf((int) ((length >>> (i * 8)) & 255)));
        }
        return arrayList;
    }


    private static int rotateLeft(int i, int i2) {
        return (i >>> (32 - i2)) | (i << i2);
    }

    public String sign(byte[] bArr) {
        ArrayList<Integer> padding = padding(bArr);
        int i = A;
        int i2 = B;
        int i3 = C;
        int i4 = D;
        for (int i5 = 0; i5 < padding.size() / 64; i5++) {
            int[] iArr = new int[16];
            for (int i6 = 0; i6 < 16; i6++) {
                int i7 = (i5 * 64) + (i6 * 4);
                iArr[i6] = (padding.get(i7 + 3).intValue() << 24) | padding.get(i7).intValue() | (padding.get(i7 + 1).intValue() << 8) | (padding.get(i7 + 2).intValue() << 16);
            }
            int[] iArr2 = {0, 4, 8, 12};
            int i8 = i;
            int i9 = i2;
            int i10 = i3;
            int i11 = i4;
            int i12 = 0;
            while (i12 < 4) {
                int i13 = iArr2[i12];
                i8 = ff(i8, i9, i10, i11, iArr[i13], 3);
                int ff = ff(i11, i8, i9, i10, iArr[i13 + 1], 7);
                i10 = ff(i10, ff, i8, i9, iArr[i13 + 2], 11);
                i9 = ff(i9, i10, ff, i8, iArr[i13 + 3], 19);
                i12++;
                i11 = ff;
            }
            int[] iArr3 = {0, 1, 2, 3};
            int i14 = i8;
            int i15 = i11;
            for (int i16 = 0; i16 < 4; i16++) {
                int i17 = iArr3[i16];
                i14 = gg(i14, i9, i10, i15, iArr[i17], 3);
                i15 = gg(i15, i14, i9, i10, iArr[i17 + 4], 5);
                i10 = gg(i10, i15, i14, i9, iArr[i17 + 8], 9);
                i9 = gg(i9, i10, i15, i14, iArr[i17 + 12], 13);
            }
            int[] iArr4 = {0, 2, 1, 3};
            int i18 = i14;
            int i19 = 0;
            while (i19 < 4) {
                int i20 = iArr4[i19];
                int hh = hh(i18, i9, i10, i15, iArr[i20], 3);
                i15 = hh(i15, hh, i9, i10, iArr[i20 + 8], 9);
                i10 = hh(i10, i15, hh, i9, iArr[i20 + 4], 11);
                i9 = hh(i9, i10, i15, hh, iArr[i20 + 12], 15);
                i19++;
                i18 = hh;
            }
            i += i18;
            i2 += i9;
            i3 += i10;
            i4 += i15;
        }
        return String.format("%02x%02x%02x%02x", Integer.valueOf(i), Integer.valueOf(i2), Integer.valueOf(i3), Integer.valueOf(i4));
    }

}




