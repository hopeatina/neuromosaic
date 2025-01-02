import { redirect } from "next/navigation";

export default function DocsPage() {
  // In development, redirect to Mintlify docs server
  if (process.env.NODE_ENV === "development") {
    redirect("http://localhost:3001");
  }

  // In production, redirect to the hosted Mintlify docs
  redirect("https://neuromosaic.mintlify.app/");
}
