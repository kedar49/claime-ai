"use client";

import Navbar from "@/components/Navbar";
import { motion } from "framer-motion";

export default function About() {
    return (
        <main className="min-h-screen bg-background text-foreground selection:bg-primary/30 overflow-x-hidden font-mono grid-bg transition-colors duration-300">
            {/* Grid Overlay */}
            <div className="fixed inset-0 z-0 pointer-events-none border-x border-border max-w-7xl mx-auto" />

            <div className="relative z-10 flex flex-col min-h-screen max-w-7xl mx-auto border-x border-border">
                <Navbar />

                <div className="flex-1 flex flex-col items-center justify-center p-8 md:p-16">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="w-full max-w-4xl space-y-12"
                    >
                        {/* Header */}
                        <div className="text-center space-y-4">
                            <h1 className="text-6xl md:text-8xl font-bold font-display uppercase tracking-tighter">
                                About Claime AI
                            </h1>
                            <p className="text-muted-foreground text-lg md:text-xl font-mono uppercase tracking-widest">
                                AI-Powered Fact Verification
                            </p>
                        </div>

                        {/* Project Information */}
                        <div className="text-center space-y-4 p-8 border border-border bg-card/50 backdrop-blur-sm">
                            <p className="text-foreground/90 text-lg leading-relaxed">
                                This is our <span className="font-bold text-primary">7th Semester Major Project</span>
                            </p>
                            <p className="text-muted-foreground text-base font-mono uppercase tracking-widest">
                                Under the guidance of
                            </p>
                            <p className="text-foreground text-xl font-bold">
                                Prof. Gopal Deshmukh Sir
                            </p>
                        </div>

                        {/* Developers */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Kedar Sathe */}
                            <div className="space-y-4 p-8 border border-border bg-card/50 backdrop-blur-sm hover:border-primary/50 transition-colors">
                                <div>
                                    <h2 className="text-3xl font-bold font-display uppercase mb-2">Kedar Sathe</h2>
                                    <p className="text-sm text-muted-foreground font-mono uppercase tracking-widest">Developer</p>
                                </div>
                                <p className="text-foreground/80 leading-relaxed">
                                    Passionate about building AI-powered solutions that make a difference. Specializing in full-stack development and machine learning applications.
                                </p>
                            </div>

                            {/* Riddhi Shende */}
                            <div className="space-y-4 p-8 border border-border bg-card/50 backdrop-blur-sm hover:border-primary/50 transition-colors">
                                <div>
                                    <h2 className="text-3xl font-bold font-display uppercase mb-2">Riddhi Shende</h2>
                                    <p className="text-sm text-muted-foreground font-mono uppercase tracking-widest">Developer</p>
                                </div>
                                <p className="text-foreground/80 leading-relaxed">
                                    Dedicated to creating innovative technology solutions. Contributing to the vision and execution of Claime AI with expertise in AI and software development.
                                </p>
                            </div>
                        </div>

                        {/* Footer Note */}
                        <div className="text-center pt-12 border-t border-border">

                        </div>

                    </motion.div>
                </div>

                <footer className="border-t border-border py-6 px-6 text-center text-xs text-muted-foreground font-mono uppercase tracking-widest">
                    Built by Kedar Sathe & Riddhi Shende
                </footer>
            </div>
        </main>
    );
}
