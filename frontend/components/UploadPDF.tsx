"use client";

import { useState } from "react";

import { uploadPDF } from "@/lib/api";


export default function UploadPDF() {

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");


  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const file = event.target.files?.[0];


    if (!file) {
      return;
    }


    if (file.type !== "application/pdf") {

      setMessage(
        "Please select a PDF file."
      );

      return;

    }


    setLoading(true);

    setMessage("");


    try {

      const data = await uploadPDF(file);

      setMessage(
        `${data.filename} uploaded successfully.`
      );

    }

    catch (error) {

      console.error(error);

      setMessage(
        "PDF upload failed."
      );

    }

    finally {

      setLoading(false);

    }

  }


  return (

    <div>

      <h2>
        Upload PDF
      </h2>


      <input
        type="file"
        accept="application/pdf"
        onChange={handleUpload}
        disabled={loading}
      />


      {loading && (

        <p>
          Uploading and indexing PDF...
        </p>

      )}


      {message && (

        <p>
          {message}
        </p>

      )}

    </div>

  );

}