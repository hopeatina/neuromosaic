import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import "@/styles/globals.css";

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      html: React.DetailedHTMLProps<
        React.HtmlHTMLAttributes<HTMLHtmlElement>,
        HTMLHtmlElement
      >;
      body: React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLBodyElement>,
        HTMLBodyElement
      >;
      main: React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement>,
        HTMLElement
      >;
    }
  }
}

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Neuromosaic - AI Model Training Platform",
  description:
    "A distributed platform for training and improving AI models through iterative refinement and community collaboration.",
  keywords: [
    "AI",
    "machine learning",
    "distributed computing",
    "model training",
    "neural networks",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
