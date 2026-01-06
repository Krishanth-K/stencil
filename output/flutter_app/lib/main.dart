
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: r'flutter_app',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(r'flutter_app'),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              Text(r"My Awesome App", style: Theme.of(context).textTheme.headlineMedium),
              Text(r"Welcome to Stencil!\nThis is a simple example of a UI defined in YAML.\n"),
              Text(r"Welcome to Stencil!\nThis is a simple example of a UI defined in YAML.\n"),
              ElevatedButton(onPressed: () {}, child: Text(r"Click Me!")),
              const Divider(),
              
TextField(
  decoration: InputDecoration(
    border: OutlineInputBorder(),
    labelText: r'Your Name',
  ),
),

              ElevatedButton(onPressed: () {}, child: Text(r"Submit")),
              Text(r"© 2025 Your Company"),
            ]
            .map((w) => Padding(padding: const EdgeInsets.symmetric(vertical: 8.0), child: w))
            .toList(),
          ),
        ),
      ),
    );
  }
}
