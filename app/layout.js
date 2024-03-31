import "./globals.css";

export const metadata = {
  title: "Chess",
  description: "Complete Chess Game and engine made by Neel",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
