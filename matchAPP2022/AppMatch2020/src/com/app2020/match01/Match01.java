package com.app2020.match01;

import java.util.ArrayList;

public class Match01 {
    public static void main(String[] args) {
        String params = "page=" + args[0] + args[1];
        String sign = sign(params); // 316fbdca2c5dd2862cc8e86281e7bda9
        // String sign = sign("page=71743861270"); // 316fbdca2c5dd2862cc8e86281e7bda9
        System.out.println(sign);
    }

    public static String sign(String input) {
        return new Sign().sign(input.getBytes());
    }
}

class Sign {

    private static final int f276A = 1732584193;
    private static final int f277B = -271733879;
    private static final int f278C = -1732584194;
    private static final int f279D = 271733878;

    private static int m184f(int i, int i2, int i3) {
        return ((~i) & i3) | (i2 & i);
    }

    private static int m185ff(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + m184f(i2, i3, i4) + i5, i6);
    }

    private static int m186g(int i, int i2, int i3) {
        return (i & i3) | (i & i2) | (i2 & i3);
    }

    private static int m187gg(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + m186g(i2, i3, i4) + i5 + 1518565785, i6);
    }

    private static int m188h(int i, int i2, int i3) {
        return (i ^ i2) ^ i3;
    }

    private static int m189hh(int i, int i2, int i3, int i4, int i5, int i6) {
        return rotateLeft(i + m188h(i2, i3, i4) + i5 + 1859775393, i6);
    }

    private ArrayList<Integer> padding(byte[] bArr) {
        long length = bArr.length * 8; // 将原本的 int 改为 long 类型
        ArrayList<Integer> arrayList = new ArrayList<>();
        for (byte b : bArr) {
            arrayList.add(Integer.valueOf(b));
        }
        arrayList.add(128);
        while (((arrayList.size() * 8) + 64) % 512 != 0) {
            arrayList.add(0);
        }
        for (int i = 0; i < 8; i++) {
            // System.out.printf("%d\n", (length >>> (i * 8)) & 255);
            arrayList.add(Integer.valueOf((int) ((length >>> (i * 8)) & 255)));
        }
        return arrayList;
    }

    private static int rotateLeft(int i, int i2) {
        return (i >>> (32 - i2)) | (i << i2);
    }

    public String sign(byte[] bArr) {
        ArrayList<Integer> padding = padding(bArr);
        int i = f276A;
        int i2 = f277B;
        int i3 = f278C;
        int i4 = f279D;
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
                i8 = m185ff(i8, i9, i10, i11, iArr[i13], 3);
                int m185ff = m185ff(i11, i8, i9, i10, iArr[i13 + 1], 7);
                i10 = m185ff(i10, m185ff, i8, i9, iArr[i13 + 2], 11);
                i9 = m185ff(i9, i10, m185ff, i8, iArr[i13 + 3], 19);
                i12++;
                i11 = m185ff;
            }
            int[] iArr3 = {0, 1, 2, 3};
            int i14 = i8;
            int i15 = i11;
            for (int i16 = 0; i16 < 4; i16++) {
                int i17 = iArr3[i16];
                i14 = m187gg(i14, i9, i10, i15, iArr[i17], 3);
                i15 = m187gg(i15, i14, i9, i10, iArr[i17 + 4], 5);
                i10 = m187gg(i10, i15, i14, i9, iArr[i17 + 8], 9);
                i9 = m187gg(i9, i10, i15, i14, iArr[i17 + 12], 13);
            }
            int[] iArr4 = {0, 2, 1, 3};
            int i18 = i14;
            int i19 = 0;
            while (i19 < 4) {
                int i20 = iArr4[i19];
                int m189hh = m189hh(i18, i9, i10, i15, iArr[i20], 3);
                i15 = m189hh(i15, m189hh, i9, i10, iArr[i20 + 8], 9);
                i10 = m189hh(i10, i15, m189hh, i9, iArr[i20 + 4], 11);
                i9 = m189hh(i9, i10, i15, m189hh, iArr[i20 + 12], 15);
                i19++;
                i18 = m189hh;
            }
            i += i18;
            i2 += i9;
            i3 += i10;
            i4 += i15;
        }
        return String.format("%02x%02x%02x%02x", Integer.valueOf(i), Integer.valueOf(i2), Integer.valueOf(i3), Integer.valueOf(i4));
    }
}
