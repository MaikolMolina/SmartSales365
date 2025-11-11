import org.gradle.api.tasks.Delete
buildscript {
    repositories {
        google()
        mavenCentral()
    }

    dependencies {
        // 🔹 Define la versión de Kotlin como variable local
        val kotlinVersion = "1.9.25"

        // 🔹 Gradle Android plugin
        classpath("com.android.tools.build:gradle:8.7.0")

        // 🔹 Kotlin Gradle plugin
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlinVersion")

        // 🔹 Plugin de Google Services (Firebase)
        classpath("com.google.gms:google-services:4.4.2")
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = file("../build")

subprojects {
    buildDir = file("${rootProject.buildDir}/${project.name}")
}
subprojects {
    project.evaluationDependsOn(":app")
}

// 🔹 Tarea de limpieza
tasks.register<Delete>("clean") {
    delete(rootProject.buildDir)
}