import 'package:flutter/material.dart';
import 'package:auth0_flutter/auth0_flutter.dart';
import 'secrets.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Auth0 Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  Auth0? auth0;
  UserProfile? userProfile;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    auth0 = Auth0(AUTH0_DOMAIN, AUTH0_CLIENT_ID);
  }

  Future<void> login() async {
    setState(() {
      isLoading = true;
    });

    try {
      final credentials = await auth0?.webAuthentication().login();
      setState(() {
        userProfile = credentials?.user;
      });
    } catch (e) {
      print('Error logging in: $e');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> logout() async {
    try {
      await auth0?.webAuthentication().logout();
      setState(() {
        userProfile = null;
      });
    } catch (e) {
      print('Error logging out: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Auth0 Flutter Demo'),
        actions: [
          if (userProfile != null)
            IconButton(
              icon: const Icon(Icons.logout),
              onPressed: logout,
            ),
        ],
      ),
      body: Center(
        child: isLoading
            ? const CircularProgressIndicator()
            : userProfile == null
                ? ElevatedButton(
                    onPressed: login,
                    child: const Text('Login'),
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('Welcome ${userProfile?.name ?? "User"}!'),
                      const SizedBox(height: 20),
                      Text('Email: ${userProfile?.email ?? ""}'),
                    ],
                  ),
      ),
    );
  }
}
