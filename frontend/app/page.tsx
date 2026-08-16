import UploadPDF from "@/components/UploadPDF";

export default function Home() {

  return (

    <div className="min-h-screen p-8">

      <div className="mx-auto max-w-5xl">

        <h1 className="text-3xl font-bold text-white">
          Upload PDF
        </h1>

        <p className="mt-2 text-gray-400">
          Add documents to your knowledge base.
        </p>

        <div className="mt-8">
          <UploadPDF />
        </div>

      </div>

    </div>

  );
}