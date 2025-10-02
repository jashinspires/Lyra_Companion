import 'package:flutter/material.dart';

class ChatScreen extends StatelessWidget {
  const ChatScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Padding(
          padding: EdgeInsets.all(16),
          child: Text(
            'Compassionate conversation',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.w600),
          ),
        ),
        const SizedBox(height: 8),
        Expanded(
          child: Center(
            child: Text(
              'Your chats will appear here.\nStart by sharing how you are feeling today.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
          ),
        ),
        const Padding(
          padding: EdgeInsets.all(16),
          child: TextField(
            decoration: InputDecoration(
              hintText: 'Type a message or feeling...',
              border: OutlineInputBorder(),
              suffixIcon: Icon(Icons.send),
            ),
          ),
        ),
      ],
    );
  }
}
