"use client";

import { useState } from "react";

import { uploadPDF } from "@/lib/api";


type Props = {
  sessionId: string;
};

export default function UploadPDF({
  sessionId,
}: Props) {

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");


  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const file =
      event.target.files?.[0];


    if (!file) {
      return;
    }


    if (
      file.type !== "application/pdf"
    ) {

      setMessage(
        "Please select a PDF file."
      );

      return;

    }


    setLoading(true);

    setMessage("");


    try {

      console.log(
        "Uploading PDF for session:",
        sessionId
      );


      const data =
        await uploadPDF(
          file,
          sessionId
        );


      setMessage(
        `${data.filename} uploaded successfully.`
      );

    }

    catch (error) {

      console.error(
        "PDF upload error:",
        error
      );


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