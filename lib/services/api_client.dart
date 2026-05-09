import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/account_model.dart';

class ApiClient {
  final String baseUrl = 'http://localhost:8000';

  Future<AccountModel> fetchAccount() async {
    final response = await http.get(Uri.parse('$baseUrl/api/account/1'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return AccountModel.fromJson(data);
    } else {
      throw Exception('Failed to load account');
    }
  }
}
