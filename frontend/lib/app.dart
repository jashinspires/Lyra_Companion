import 'package:flutter/material.dart';

import 'screens/home/home_shell.dart';

class LyraApp extends StatelessWidget {
  const LyraApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lyra Companion',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF5D5FEF)),
        useMaterial3: true,
      ),
      home: const HomeShell(),
    );
  }
}
