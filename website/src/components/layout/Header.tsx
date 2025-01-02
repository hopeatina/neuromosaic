"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Logo } from "@/components/ui/Logo";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { WaitlistForm } from "@/components/forms/WaitlistForm";
import { cn } from "@/library/utils";

const navigation = [
  { name: "About", href: "/about" },
  { name: "Flywheel", href: "/flywheel" },
  { name: "Updates", href: "/updates" },
  { name: "Get Involved", href: "/get-involved" },
  { name: "Distributed", href: "/distributed" },
];

// Pages with light backgrounds that need dark text
const LIGHT_BACKGROUND_PAGES = ["/about", "/flywheel", "/updates"];

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isWaitlistOpen, setIsWaitlistOpen] = useState(false);
  const pathname = usePathname();

  const isLightBackground = LIGHT_BACKGROUND_PAGES.includes(pathname);

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      setIsScrolled(scrollPosition > 0);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const getTextColorClasses = (isLink = false) => {
    if (isScrolled) {
      return isLink
        ? "text-neutral-600 hover:text-neutral-900"
        : "text-neutral-900";
    }

    if (isLightBackground) {
      return isLink
        ? "text-neutral-600 hover:text-neutral-900"
        : "text-neutral-900";
    }

    return isLink ? "text-neutral-200 hover:text-white" : "text-white";
  };

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 h-header border-b transition-colors duration-200",
        isScrolled
          ? "header-solid"
          : isLightBackground
          ? "bg-white/80 backdrop-blur-sm border-gray-200"
          : "header-transparent"
      )}
    >
      <Modal
        isOpen={isWaitlistOpen}
        onOpenChange={setIsWaitlistOpen}
        size="wide"
      >
        <WaitlistForm onSuccess={() => setIsWaitlistOpen(false)} />
      </Modal>

      <Container className="flex h-full items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <Logo
              size="sm"
              variant={isScrolled || isLightBackground ? "dark" : "light"}
            />
            <span
              className={cn(
                "font-semibold transition-colors duration-200",
                getTextColorClasses()
              )}
            >
              Neuromosaic
            </span>
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "text-sm font-medium transition-colors duration-200",
                  getTextColorClasses(true)
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/docs" className="inline-block">
            <Button
              variant="ghost"
              size="sm"
              className={cn(
                "transition-colors duration-200",
                getTextColorClasses(true),
                isLightBackground && !isScrolled
                  ? "hover:bg-gray-100"
                  : "hover:bg-white/10"
              )}
            >
              Docs
            </Button>
          </Link>
          <Button
            size="sm"
            className={cn(
              "transition-colors duration-200",
              isScrolled || isLightBackground
                ? "bg-primary text-white hover:bg-primary/90"
                : "bg-white/10 text-white hover:bg-white hover:text-background-dark"
            )}
            onClick={() => setIsWaitlistOpen(true)}
          >
            Join Waitlist
          </Button>
        </div>
      </Container>
    </header>
  );
}
