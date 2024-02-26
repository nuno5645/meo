import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(ModernGridApp());
}

class ModernGridApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Modern Grid App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  List<Product> products = [];
  int pointsBalance = 0;

  @override
  void initState() {
    super.initState();
    fetchProducts();
    fetchPointsBalance();
  }

  Future<void> fetchProducts() async {
    try {
      final response = await http.get(
        Uri.parse('https://dace89d1-c1aa-4299-bfbf-bd91ab2cf517.mock.pstmn.io/api/scrape_data/'),
      );
      if (response.statusCode == 200) {
        final List<dynamic> productJson = json.decode(response.body);
        setState(() {
          products = productJson.map((json) => Product.fromJson(json)).toList();
        });
      } else {
        print('Failed to load products. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Failed to load products. Error: $e');
    }
  }

  Future<void> fetchPointsBalance() async {
    try {
      final response = await http.get(
        Uri.parse('https://e7b1799e-8bc6-4c66-a11e-f9b932970994.mock.pstmn.io/api/points/'),
      );
      if (response.statusCode == 200) {
        final Map<String, dynamic> pointsJson = json.decode(response.body);
        setState(() {
          pointsBalance = pointsJson['points'];
        });
      } else {
        print('Failed to load points balance. Status code: ${response.statusCode}');
      }
    } catch (e) {
      print('Failed to load points balance. Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Ofertas MEO'),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              fetchProducts();
              fetchPointsBalance();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            GridView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                childAspectRatio: 0.9,
              ),
              itemCount: products.length,
              itemBuilder: (context, index) {
                return InkWell(
                  onTap: () {
                    // Navigate to a detailed page or take action
                    // For now, print product name when tapped
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => ProductDetailScreen(product: products[index])),
                    );
                  },
                  child: ProductCard(product: products[index]),
                );
              },
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Points Balance: $pointsBalance'),
            ),
          ],
        ),
      ),
    );
  }
}

class Product {
  final int id;
  final String name;
  final String imageUrl;
  final double pointsCost;
  final bool available;
  final String description;
  final String linkUrl;
  final int stock;

  Product({
    required this.id,
    required this.name,
    required this.imageUrl,
    required this.pointsCost,
    required this.available,
    required this.description,
    required this.linkUrl,
    required this.stock,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      imageUrl: json['image_url'],
      pointsCost: json['points_cost'].toDouble(),
      available: json['available'],
      description: json['description'],
      linkUrl: json['link_url'],
      stock: json['stock'],
    );
  }
}

class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({Key? key, required this.product}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SingleChildScrollView(  // Add this
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            SizedBox(
              width: double.infinity,
              height: 300, // Adjust the height of the image
              child: Image.network(
                product.imageUrl,
                fit: BoxFit.cover, // Adjusted fit property
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(product.name, style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }
}



class ProductDetailScreen extends StatelessWidget {
  final Product product;

  const ProductDetailScreen({Key? key, required this.product}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(product.name),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: SingleChildScrollView(  // Add this
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                width: double.infinity,
                child: Image.network(
                  product.imageUrl,
                  height: 400,
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(product.name, style: TextStyle(fontWeight: FontWeight.bold)),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Text('Points Cost: ${product.pointsCost}'),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Text('Description: ${product.description}'),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Text('Stock: ${product.stock}'),
              ),
              ListTile(
                leading: Icon(product.available ? Icons.check_circle_outline : Icons.highlight_off),
                title: Text(product.available ? 'Available' : 'Not Available'),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: ElevatedButton(
                  onPressed: () async {
                    final Uri uri = Uri.parse('https://loja.meo.pt/Equipamentos/sensacoes/Altice/Convite-Duplo-Portugal-Coreia-do-Sul-27nov?cor=NA&modo-compra=Points');
                    if (await canLaunchUrl(uri)) {
                      await launchUrl(uri);
                    } else {
                      // Using SnackBar to show the error message
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Could not launch the URL'),
                        ),
                      );
                      // Logging the error
                      print('Could not launch the URL');
                    }
                  },
                  child: Text('Go to Product'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
