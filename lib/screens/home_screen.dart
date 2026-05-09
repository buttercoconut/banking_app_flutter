import 'package:flutter/material.dart';
import '../widgets/custom_app_bar.dart';
import '../services/api_client.dart';
import '../models/account_model.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<AccountModel> _accountFuture;

  @override
  void initState() {
    super.initState();
    _accountFuture = ApiClient().fetchAccount();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Home'),
      body: Center(
        child: FutureBuilder<AccountModel>(
          future: _accountFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            }
            if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            }
            final account = snapshot.data!;
            return Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('Account Number: ${account.accountNumber}',
                    style: const TextStyle(fontSize: 18)),
                const SizedBox(height: 8),
                Text('Balance: ${account.balance.toStringAsFixed(2)}',
                    style: const TextStyle(fontSize: 18)),
              ],
            );
          },
        ),
      ),
    );
  }
}
