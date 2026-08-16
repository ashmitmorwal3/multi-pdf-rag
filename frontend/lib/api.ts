// Production backend configured through NEXT_PUBLIC_API_URL

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";


// ==============================
// ASK QUESTION
// ==============================

export async function askQuestion(
  sessionId: string,
  question: string,
  documents: string[]
) {

  const response = await fetch(
    `${API_URL}/ask`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        session_id: sessionId,
        question: question,
        documents: documents,
      }),
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    console.error(
      "Backend error:",
      errorText
    );

    throw new Error(
      `Request failed: ${response.status} - ${errorText}`
    );

  }


  return response.json();

}


// ==============================
// UPLOAD PDF
// ==============================

export async function uploadPDF(
  file: File,
  sessionId: string
) {

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );

  formData.append(
    "session_id",
    sessionId
  );


  const response = await fetch(
    `${API_URL}/upload`,
    {
      method: "POST",

      body: formData,
    }
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    console.error(
      "Upload error:",
      errorText
    );

    throw new Error(
      `Upload failed: ${response.status} - ${errorText}`
    );

  }


  return response.json();

}


// ==============================
// GET DOCUMENTS FOR SESSION
// ==============================

export async function getDocuments(
  sessionId: string
): Promise<string[]> {

  const response = await fetch(
    `${API_URL}/documents?session_id=${encodeURIComponent(sessionId)}`
  );


  if (!response.ok) {

    const errorText =
      await response.text();

    console.error(
      "Documents error:",
      errorText
    );

    throw new Error(
      `Failed to fetch documents: ${response.status} - ${errorText}`
    );

  }


  const data =
    await response.json();


  return data.documents;

}