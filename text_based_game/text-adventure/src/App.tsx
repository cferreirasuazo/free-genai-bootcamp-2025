"use client";

import type React from "react";

import { useState, useRef, useEffect } from "react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { ScrollArea } from "./components/ui/scroll-area";
import { Send, BookOpen } from "lucide-react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";

function App() {
  const [gameText, setGameText] = useState<string[]>([
    "Welcome to the Text Adventure Game!",
    "You find yourself standing at the entrance of a dark cave. The wind howls behind you, and a faint glow emanates from deep within.",
    "What would you like to do?",
  ]);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<
    { command: string; response: string }[]
  >([]);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Sample game logic - in a real game, this would be more complex
  // const processCommand = (command: string) => {
  //   let response = "";

  //   const lowerCommand = command.toLowerCase();

  //   if (lowerCommand.includes("look") || lowerCommand.includes("examine")) {
  //     response =
  //       "The cave entrance is dark and foreboding. Stalactites hang from the ceiling, and the ground is damp. The air smells of earth and something... unfamiliar.";
  //   } else if (
  //     lowerCommand.includes("enter") ||
  //     lowerCommand.includes("go in") ||
  //     lowerCommand.includes("forward")
  //   ) {
  //     response =
  //       "You cautiously step into the cave. The temperature drops noticeably. Your footsteps echo against the stone walls. A few yards in, the path splits in two directions.";
  //   } else if (
  //     lowerCommand.includes("leave") ||
  //     lowerCommand.includes("exit") ||
  //     lowerCommand.includes("turn back")
  //   ) {
  //     response =
  //       "You decide to turn back, but as you do, a sudden gust of wind pushes you forward, and rocks tumble down, blocking the entrance. It seems going back is no longer an option.";
  //   } else if (lowerCommand.includes("help")) {
  //     response =
  //       "Try commands like: look, examine, enter, go in, leave, exit, turn back, inventory, take, drop, etc.";
  //   } else if (lowerCommand.trim() === "") {
  //     response = "Please enter a command.";
  //   } else {
  //     response =
  //       "I don't understand that command. Try something else or type 'help' for suggestions.";
  //   }

  //   return response;
  // };

  const processCommand = async (command: string) => {
    const sessionId = "81e35acf-43d5-43ec-8da0-94310b070864"; // Replace with a valid session ID
    const gameResponse = await sendUserInput(sessionId, command);
    return gameResponse;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (input.trim() === "") return;

    const response = await processCommand(input);
    const newHistoryItem = { command: input, response };

    setHistory([...history, newHistoryItem]);
    setGameText([...gameText, `> ${input}`, response]);
    setInput("");
  };

  // Auto-scroll to the bottom when new text is added
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector(
        "[data-radix-scroll-area-viewport]"
      );
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [gameText]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50">
      <Card className="max-w-2xl w-full h-[600px] flex flex-col shadow-lg">
        <CardHeader className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
          <CardTitle className="text-center flex items-center justify-center gap-2">
            <BookOpen className="h-5 w-5" />
            Text Adventure
          </CardTitle>
        </CardHeader>

        <CardContent className="flex-1 p-0 overflow-hidden">
          <ScrollArea className="h-full p-6" ref={scrollAreaRef}>
            <div className="space-y-4">
              {gameText.map((text, index) => (
                <div key={index} className="leading-relaxed">
                  {text.startsWith(">") ? (
                    <div className="flex gap-2 items-start mt-4">
                      <div className="bg-primary/10 p-2 rounded-lg text-primary font-medium">
                        {text.substring(2)}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-muted/30 p-3 rounded-lg shadow-sm">
                      {text}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>

        <CardFooter className="p-4 border-t">
          <form onSubmit={handleSubmit} className="flex w-full gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="What will you do next?"
              className="flex-1"
            />
            <Button type="submit" size="icon">
              <Send className="h-4 w-4" />
              <span className="sr-only">Submit</span>
            </Button>
          </form>
        </CardFooter>
      </Card>
    </div>
  );
}

export default App;
