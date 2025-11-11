import java.util.Properties

plugins {
    id("com.android.application")
    id("kotlin-android")
    id("com.google.gms.google-services") // ✅ Firebase
    id("dev.flutter.flutter-gradle-plugin") // ✅ Flutter plugin (último)
}

// --- 🔹 Cargar propiedades desde local.properties ---
val localProperties = Properties()
val localPropertiesFile = rootProject.file("local.properties")
if (localPropertiesFile.exists()) {
    localProperties.load(localPropertiesFile.reader(Charsets.UTF_8))
}

val flutterRoot = localProperties.getProperty("flutter.sdk")
    ?: throw GradleException("Flutter SDK not found. Define location with flutter.sdk in local.properties")

val flutterVersionCode = localProperties.getProperty("flutter.versionCode")?.toIntOrNull() ?: 1
val flutterVersionName = localProperties.getProperty("flutter.versionName") ?: "1.0"

// --- 🔹 Configuración de Android ---
android {
    namespace = "com.example.smartsales365_mobile"
    compileSdk = 36 // ✅ Requerido por shared_preferences_android

    ndkVersion = flutter.ndkVersion

    defaultConfig {
        applicationId = "com.example.smartsales365_mobile"
        minSdk = flutter.minSdkVersion
        targetSdk = 36
        versionCode = flutterVersionCode
        versionName = flutterVersionName
        multiDexEnabled = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
        isCoreLibraryDesugaringEnabled = true // ✅ Necesario para notificaciones locales
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    sourceSets {
        getByName("main").java.srcDirs("src/main/kotlin")
    }

    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("debug") // Cambiar al firmar
        }
    }
}

flutter {
    source = "../.."
}

// --- 🔹 Dependencias ---
dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib:1.9.25")

    // ✅ Firebase
    implementation(platform("com.google.firebase:firebase-bom:33.5.1"))
    implementation("com.google.firebase:firebase-analytics")
    implementation("com.google.firebase:firebase-messaging")

    // ✅ Multidex
    implementation("androidx.multidex:multidex:2.0.1")

    // ✅ Desugaring actualizado
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
}
