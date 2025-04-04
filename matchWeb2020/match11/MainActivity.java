package com.yuanrenxue.app.web2020.match11;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.util.Random;

public class MainActivity {

    // 配置常量
    public static final boolean STEP_LOG = false;
    public static final Boolean LOGGING = false;
    public static final boolean JAR_CALL = false; // 打包成jar之前设置为true
    public static final String TARGET_PROCESS = "com.yuanrenxue.onlinejudge2020"; // 进程名
    public static final String NATIVE_LIB_NAME = "libyuanrenxue_native.so"; // 调用的so文件名
    public static final int ANDROID_API_LEVEL = 23;

    // 实例变量
    public AndroidEmulator emulator;
    public DvmClass dvmClass;

    MainActivity() {
        emulator = AndroidEmulatorBuilder
                .for64Bit()
                .setProcessName(TARGET_PROCESS)
                .build();

        Memory memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(ANDROID_API_LEVEL));

        VM vm = emulator.createDalvikVM();
        vm.setVerbose(LOGGING);
        vm.setJni(new AbstractJni() {
            @Override
            public DvmObject<?> newObjectV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
                if ("java/util/Random-><init>()V".equals(signature)) {
                    if (STEP_LOG) System.out.println(1);
                    return vm.resolveClass("java/util/Random").newObject(new Random());
                }
                if ("java/util/Random-><init>(J)V".equals(signature)) {
                    if (STEP_LOG) System.out.println(5);
                    return vm.resolveClass("java/util/Random").newObject(new Random(vaList.getLongArg(0)));
                }
                return super.newObjectV(vm, dvmClass, signature, vaList);
            }

            @Override
            public int callIntMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
                if ("java/util/Random->nextInt(I)I".equals(signature)) {
                    if (STEP_LOG) System.out.println(2);
                    Random random = (Random) dvmObject.getValue();
                    return random.nextInt(vaList.getIntArg(0));
                }
                return super.callIntMethodV(vm, dvmObject, signature, vaList);
            }

            @Override
            public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
                if ("android/content/ContextWrapper->getFilesDir()Ljava/io/File;".equals(signature)) {
                    if (STEP_LOG) System.out.println(3);
                    return vm.resolveClass("java/io/File").newObject(new File("/"));
                }
                return super.callObjectMethodV(vm, dvmObject, signature, vaList);
            }

            @Override
            public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
                if ("android/os/Looper->myLooper()Landroid/os/Looper;".equals(signature)) {
                    if (STEP_LOG) System.out.println(4);
                    return vm.resolveClass("android/os/Looper").newObject(null);
                }
                return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
            }
        });

        DalvikModule dalvikModule;
        if (JAR_CALL) {
            dalvikModule = vm.loadLibrary(new File(NATIVE_LIB_NAME), false);
        } else {
            dalvikModule = vm.loadLibrary(new File("unidbg-android/src/test/java/com/yuanrenxue/app/web2020/match11/libyuanrenxue_native.so"), false);
        }
        Module module = dalvikModule.getModule();

        DvmClass contextWrapper = vm.resolveClass("android/content/ContextWrapper");
        dvmClass = vm.resolveClass("com/yuanrenxue/onlinejudge2020/OnlineJudgeApp", contextWrapper);

        vm.callJNI_OnLoad(emulator, module);
    }

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        MainActivity mainActivity = new MainActivity();
        long endTime = System.currentTimeMillis();
        if (LOGGING) System.out.println("load time: " + (endTime - startTime) + "ms");

        String sign;
        if (JAR_CALL) {
            sign = mainActivity.getSign(args[0]);
        } else {
            sign = mainActivity.getSign("1");
        }
        System.out.println(sign);
    }

    public String getSign(String num) {
        DvmObject<?> dvmObject = dvmClass.newObject(null);
        DvmObject<?> signObj = dvmObject.callJniMethodObject(emulator, "getSign(J)Ljava/lang/String;", num);
        return (String) signObj.getValue();
    }

}