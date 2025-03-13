async function sendUserInput(
  sessionId: string,
  userText: string
): Promise<string> {
  const apiUrl = "http://127.0.0.1:8000/play/";

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ session_id: sessionId, user_text: userText }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    return data["game_master"];
  } catch (error) {
    console.error("Error communicating with the API:", error);
    throw error;
  }
}

export default sendUserInput;

// // Example usage
// (async () => {
//   try {
//     const sessionId = "81e35acf-43d5-43ec-8da0-94310b070864"; // Replace with a valid session ID
//     const userText = "Start";
//     const gameResponse = await sendUserInput(sessionId, userText);
//     console.log("Game Response:", gameResponse);
//   } catch (error) {
//     console.error("Failed to get game response:", error);
//   }
// })();
