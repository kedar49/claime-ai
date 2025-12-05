"use client";

import Link from "next/link";
import { ModeToggle } from "@/components/mode-toggle";

interface NavbarProps {
    onReset?: () => void;
}

export default function Navbar({ onReset }: NavbarProps) {
    return (
        <nav className="flex items-center justify-between px-6 py-6 border-b border-border bg-background/50 backdrop-blur-sm sticky top-0 z-50">
            <div
                className="text-2xl font-bold tracking-tighter flex items-center gap-2 cursor-pointer font-display"
                onClick={onReset}
            >
                <Link href="/" className="flex items-center gap-2">
                    <span className="text-foreground">CLAIME</span>
                    <span className="text-muted-foreground">.</span>
                    <span className="text-foreground">AI</span>
                </Link>
            </div>
            <div className="flex items-center gap-8 font-mono text-xs uppercase tracking-widest">
                <Link href="/about" className="text-muted-foreground hover:text-foreground transition-colors">About</Link>
                <ModeToggle />
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            </div>
        </nav>
    );
}
