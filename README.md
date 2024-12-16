- 👋 Hi, I’m @josephshih1
- 👀 I’m interested in ...
- 🌱 I’m currently learning ...
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
Ex. Passing data between screens
//main.dart
import 'package:flutter/material.dart';
import 'screen0.dart';
import 'screen1.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Named route navigation',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green,),
      darkTheme: ThemeData.dark(),
      home: Screen0(),
      initialRoute: '0',
      routes: {
        '0':(context)=>Screen0(),
        //'1':(context)=>Screen1(FirstName:""),
        '1':(context)=>Screen1(test1:[],),
      },
    );
  }
}

//screen0.dart
import 'package:flutter/material.dart';
import 'screen1.dart';

class Screen0 extends StatelessWidget {
  Screen0({super.key});

  List t1=[1,2,3];

  Future ReceiveData(BuildContext context) async {
    //final result=await Navigator.push(context, MaterialPageRoute(builder: (context)=>Screen1(FirstName:'Bob')));
    final result=await Navigator.push(context, MaterialPageRoute(builder: (context)=>Screen1(test1:t1,)));
    print(result);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Screen 0'),),
      body: Center(
        child: Column(
          children: [
            ElevatedButton(
                onPressed: ()=>ReceiveData(context),
                child: Text('Go to Screen 1'),),
          ],
        ),
      ),
    );
  }
}

//screen1.dart
import 'package:flutter/material.dart';

class Screen1 extends StatelessWidget {
  //String FirstName='';
  //Screen1({Key? key, required this.FirstName}):super(key:key);
  List test1=[];
  Screen1({Key? key, required this.test1}):super(key:key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(test1[0].toString()),),
      body: Center(
        child: Column(
          children: [
            ElevatedButton(
              onPressed: ()=>Navigator.pop(context, 'I see'),
              child: Text('Retuen'),),
          ],
        ),
      ),
    );
  }
}

Ex. Clip path example 1
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ClipPath example',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green,),
      home: ClipOvalExamples(),
    );
  }
}

class ClipOvalExamples extends StatelessWidget {
  const ClipOvalExamples({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('ClipPath example'),),
      backgroundColor: Colors.red.shade100,
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              ClipPath(
                clipper: ClipperPath1(),
                child: Container(
                  height: 600,
                  color: Colors.amber,
                ),
              ),
              SizedBox(height: 20,),
              ClipOval(
                //clipper: ,
                child: Image.asset('assets/rab1.jpg'),
              ),
              SizedBox(height: 20,),
              ClipOval(
                clipper: ClipperOvalPath(),
                child: Image.asset('assets/rab1.jpg'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ClipperOvalPath extends CustomClipper<Rect> {

  @override
  Rect getClip(Size size) {
    return Rect.fromLTRB(50, 50, size.width-20, size.height-50);
  }

  @override
  bool shouldReclip(CustomClipper<Rect> oldClipper)=>false;
}

class ClipperPath1 extends CustomClipper<Path> {

  @override
  Path getClip(Size size) {
    Path path=Path();
    path.moveTo(size.width, 0);
    path.lineTo(0,0);
    path.quadraticBezierTo(0, size.height*0.45, 0, size.height*0.6);
    path.cubicTo(size.width*0.3, size.height*0.9, size.width*0.7, size.height*0.3, size.width*1, size.height*0.6);
    path.quadraticBezierTo(size.width, size.height*0.45, size.width, 0);
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper)=>false;
}

Ex. Clip path example 2
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ClipPath example',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green,),
      home: ClipOvalExamples(),
    );
  }
}

class ClipOvalExamples extends StatelessWidget {
  const ClipOvalExamples({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('ClipPath example'),),
      backgroundColor: Colors.red.shade100,
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              ClipPath(
                clipper: ClipperPath1(),
                child: Container(
                  height: 200,
                  width: 300,
                  color: Colors.amber,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class ClipperPath1 extends CustomClipper<Path> {

  @override
  Path getClip(Size size) {
    Path path=Path();
    path.lineTo(10,size.height);
    path.lineTo(20,size.height-50);
    path.lineTo(150,size.height);
    path.lineTo(size.width,0);
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper)=>false;
}

Ex. TextSpan
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ClipPath example',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green,),
      home: ClipOvalExamples(),
    );
  }
}

class ClipOvalExamples extends StatelessWidget {
  const ClipOvalExamples({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('ClipPath example'),),
      backgroundColor: Colors.red.shade100,
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                padding: EdgeInsets.all(35),
                margin: EdgeInsets.all(20),
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.black, width:5,),
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(color: Colors.green,
                              offset: Offset(6,6),
                              blurRadius: 20,
                              spreadRadius: 5),
                  ],
                ),
                child: Text("Hello, I'm in the Container widget decoration box!",
                            style: TextStyle(fontSize: 30),),
              ),
              Text('Hello world! This is a Text widget',
                   style: TextStyle(fontSize: 35,
                                    color: Color.fromRGBO(178, 0, 237, 1),
                                    backgroundColor: Colors.yellow,
                                    fontWeight: FontWeight.w700,
                                    fontStyle: FontStyle.italic,
                                    letterSpacing: 8,
                                    wordSpacing: 5,
                                    shadows: [
                                      Shadow(color: Colors.blueAccent,
                                             offset: Offset(2,1),
                                             blurRadius: 2,),
                                    ],),),
              SizedBox(height: 20,),
              RichText(text: TextSpan(
                text: 'Don\'t have an account? ',
                style: TextStyle(color: Colors.black, fontSize: 20),
                children: [
                  TextSpan(text: 'Sign up',
                           style: TextStyle(color: Colors.blueAccent, fontSize: 20),
                           recognizer: TapGestureRecognizer()..onTap=()=>print('O')),
                ],
              ),),
              SizedBox(height: 20,),
              RichText(text: TextSpan(
                style: Theme.of(context).textTheme.bodyMedium,
                children: [
                  TextSpan(text: 'Click ', style: TextStyle(fontSize: 25),),
                  WidgetSpan(child:
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 2,),
                      child: GestureDetector(
                              child: Icon(Icons.add, color: Colors.red,),
                              onTap: ()=>print('X'),
                             ),
                      ),
                  ),
                  TextSpan(text: ' to add', style: TextStyle(fontSize: 25),),
                ],
              ),),
            ],
          ),
        ),
      ),
    );
  }
}
