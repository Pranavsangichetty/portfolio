// App.tsx
import * as React from "react";
import {
  Mail,
  Github,
  Linkedin,
  FileText,
  Upload,
  ExternalLink,
  Menu,
  X,
  ArrowRightCircle,
  Award,
  Send,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Toaster } from "@/components/ui/toaster";
import { useToast } from "@/components/ui/use-toast";

type Resume = {
  id: number;
  title: string;
  type: string;
  url: string;
};

type Project = {
  id: number;
  title: string;
  description: string;
  link?: string;
};

type Certificate = {
  id: number;
  name: string;
  url: string;
};

const initialResumes: Resume[] = [
  {
    id: 1,
    title: "Data Science Resume",
    type: "DS",
    url: "/resumes/data-science-resume.pdf",
  },
  {
    id: 2,
    title: "Data Analytics Resume",
    type: "DA",
    url: "/resumes/data-analytics-resume.pdf",
  },
  {
    id: 3,
    title: "General Tech Resume",
    type: "General",
    url: "/resumes/general-tech-resume.pdf",
  },
];

const initialProjects: Record<string, Project[]> = {
  "data-science": [
    {
      id: 1,
      title: "Customer Churn Prediction",
      description: "Predict churn using supervised learning and feature engineering.",
      link: "#",
    },
  ],
  "ai-llms": [
    {
      id: 2,
      title: "LLM-Powered Chatbot",
      description: "Domain-specific assistant for answering business queries.",
      link: "#",
    },
  ],
  "machine-learning": [
    {
      id: 3,
      title: "Lead Scoring Model",
      description: "Logistic regression model to rank and prioritize sales leads.",
      link: "#",
    },
  ],
  "data-analytics": [
    {
      id: 4,
      title: "Sales Performance Dashboard",
      description: "Interactive dashboard for tracking KPIs across regions.",
      link: "#",
    },
  ],
};

const sectionClasses = "max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16";

export default function App() {
  const { toast } = useToast();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const [resumes, setResumes] = React.useState<Resume[]>(initialResumes);
  const [editingResume, setEditingResume] = React.useState<Resume | null>(null);

  const [projectsByCategory, setProjectsByCategory] =
    React.useState<Record<string, Project[]>>(initialProjects);

  const [certificates, setCertificates] = React.useState<Certificate[]>([]);

  const [contactForm, setContactForm] = React.useState({
    name: "",
    email: "",
    message: "",
  });

  const scrollToSection = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
    setMobileOpen(false);
  };

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock submit
    toast({
      title: "Message sent",
      description: "Your message has been recorded (mock). I’ll follow up via email.",
    });
    setContactForm({ name: "", email: "", message: "" });
  };

  const handleResumeSave = (resume: Resume) => {
    setResumes((prev) => {
      const exists = prev.find((r) => r.id === resume.id);
      if (exists) {
        return prev.map((r) => (r.id === resume.id ? resume : r));
      }
      return [...prev, resume];
    });
    setEditingResume(null);
  };

  const handleResumeDelete = (id: number) => {
    setResumes((prev) => prev.filter((r) => r.id !== id));
  };

  const handleProjectUpload = (categoryKey: string, files: FileList | null) => {
    if (!files) return;
    const newProjects: Project[] = [];
    Array.from(files).forEach((file, index) => {
      const url = URL.createObjectURL(file);
      newProjects.push({
        id: Date.now() + index,
        title: file.name,
        description: "Uploaded project file from your system.",
        link: url,
      });
    });

    setProjectsByCategory((prev) => ({
      ...prev,
      [categoryKey]: [...(prev[categoryKey] || []), ...newProjects],
    }));
  };

  const handleCertificateUpload = (files: FileList | null) => {
    if (!files) return;
    const newCerts: Certificate[] = [];
    Array.from(files).forEach((file, idx) => {
      const url = URL.createObjectURL(file);
      newCerts.push({
        id: Date.now() + idx,
        name: file.name,
        url,
      });
    });
    setCertificates((prev) => [...prev, ...newCerts]);
  };

  const dsResume = resumes.find((r) => r.type === "DS");
  const daResume = resumes.find((r) => r.type === "DA");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Toaster />
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
          <div
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => scrollToSection("hero")}
          >
            <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-500" />
            <span className="font-semibold tracking-tight text-slate-50">
              Pranav Sangichetty
            </span>
          </div>

          <nav className="hidden md:flex items-center gap-6 text-sm">
            <button onClick={() => scrollToSection("resumes")} className="hover:text-sky-400">
              Resumes
            </button>
            <button onClick={() => scrollToSection("projects")} className="hover:text-sky-400">
              Projects
            </button>
            <button onClick={() => scrollToSection("certificates")} className="hover:text-sky-400">
              Certificates
            </button>
            <button onClick={() => scrollToSection("contact")} className="hover:text-sky-400">
              Contact
            </button>
          </nav>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              className="hidden sm:inline-flex border-sky-500/50 text-sky-400 hover:bg-sky-500/10"
              onClick={() => {
                // Open both DS & DA resumes if they exist
                if (dsResume?.url) window.open(dsResume.url, "_blank");
                if (daResume?.url) window.open(daResume.url, "_blank");
              }}
            >
              <FileText className="h-4 w-4 mr-1.5" />
              View Resume
            </Button>

            <button
              className="md:hidden inline-flex items-center justify-center rounded-lg border border-slate-700 p-1.5 hover:bg-slate-800"
              onClick={() => setMobileOpen((o) => !o)}
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Mobile nav */}
        {mobileOpen && (
          <div className="md:hidden border-t border-slate-800 bg-slate-950/95 backdrop-blur">
            <div className="px-4 py-3 flex flex-col gap-2 text-sm">
              <button
                className="text-left py-1 hover:text-sky-400"
                onClick={() => scrollToSection("resumes")}
              >
                Resumes
              </button>
              <button
                className="text-left py-1 hover:text-sky-400"
                onClick={() => scrollToSection("projects")}
              >
                Projects
              </button>
              <button
                className="text-left py-1 hover:text-sky-400"
                onClick={() => scrollToSection("certificates")}
              >
                Certificates
              </button>
              <button
                className="text-left py-1 hover:text-sky-400"
                onClick={() => scrollToSection("contact")}
              >
                Contact
              </button>
              <Button
                variant="outline"
                size="sm"
                className="mt-2 border-sky-500/50 text-sky-400 hover:bg-sky-500/10"
                onClick={() => {
                  if (dsResume?.url) window.open(dsResume.url, "_blank");
                  if (daResume?.url) window.open(daResume.url, "_blank");
                }}
              >
                <FileText className="h-4 w-4 mr-1.5" />
                View Resume
              </Button>
            </div>
          </div>
        )}
      </header>

      {/* HERO */}
      <section
        id="hero"
        className="relative overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950"
      >
        <div className={`${sectionClasses} flex flex-col lg:flex-row items-center gap-10 lg:gap-16`}>
          <div className="flex-1 space-y-6">
            <Badge className="bg-sky-500/10 border-sky-500/40 text-sky-300 px-3 py-1 rounded-full">
              Data Science · Machine Learning · Analytics
            </Badge>

            <div className="space-y-2">
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-semibold tracking-tight text-slate-50">
                Pranav Sangichetty
              </h1>
              <p className="text-lg sm:text-xl text-slate-300">
                Aspiring Data Scientist & Machine Learning Engineer
              </p>
            </div>

            <p className="max-w-xl text-slate-300 leading-relaxed text-sm sm:text-base">
              I build data-driven solutions across analytics, machine learning, and AI. From
              dashboards and ETL workflows to predictive models and LLM-powered tools, I focus on
              clean data, clear insights, and practical impact.
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <Button
                size="lg"
                className="rounded-xl bg-sky-600 hover:bg-sky-500 text-white"
                onClick={() => scrollToSection("projects")}
              >
                View Projects
                <ArrowRightCircle className="h-4 w-4 ml-2" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="rounded-xl border-slate-600 text-slate-100 hover:bg-slate-800"
                onClick={() => scrollToSection("contact")}
              >
                Get In Touch
              </Button>
            </div>

            <div className="flex flex-wrap items-center gap-4 pt-2 text-sm text-slate-300">
              <a
                href="mailto:your.email@example.com"
                className="inline-flex items-center gap-2 hover:text-sky-400"
              >
                <Mail className="h-4 w-4" />
                your.email@example.com
              </a>
              <a
                href="https://github.com/your-github"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 hover:text-sky-400"
              >
                <Github className="h-4 w-4" />
                GitHub
              </a>
              <a
                href="https://www.linkedin.com/in/your-linkedin"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 hover:text-sky-400"
              >
                <Linkedin className="h-4 w-4" />
                LinkedIn
              </a>
            </div>
          </div>

          <div className="flex-1 flex justify-center lg:justify-end">
            <div className="relative">
              <div className="absolute -inset-1 rounded-3xl bg-gradient-to-br from-sky-500/40 via-indigo-500/40 to-purple-500/40 blur-xl opacity-70" />
              <div className="relative h-48 w-48 sm:h-56 sm:w-56 rounded-3xl bg-slate-900/80 border border-sky-500/40 flex flex-col items-center justify-center shadow-xl">
                <div className="h-20 w-20 rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-500 flex items-center justify-center text-3xl font-semibold text-slate-50">
                  P
                </div>
                <p className="mt-3 text-sm text-slate-300 text-center px-4">
                  Placeholder professional photo. Replace with your real headshot.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* RESUMES */}
      <section id="resumes" className={sectionClasses}>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50">Featured Resumes</h2>
            <p className="text-sm text-slate-400 mt-1">
              Manage your core resumes and add more versions for different roles.
            </p>
          </div>

          <Dialog
            open={!!editingResume && editingResume.id === 0}
            onOpenChange={(open) => {
              if (!open) setEditingResume(null);
            }}
          >
            <DialogTrigger asChild>
              <Button
                size="sm"
                className="rounded-lg bg-sky-600 hover:bg-sky-500 flex items-center gap-2"
                onClick={() =>
                  setEditingResume({
                    id: 0,
                    title: "",
                    type: "",
                    url: "",
                  })
                }
              >
                Add more
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-slate-950 border-slate-800">
              <DialogHeader>
                <DialogTitle>Add New Resume</DialogTitle>
              </DialogHeader>
              {editingResume && editingResume.id === 0 && (
                <ResumeForm
                  resume={editingResume}
                  onSave={handleResumeSave}
                  onCancel={() => setEditingResume(null)}
                />
              )}
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {resumes.map((resume) => (
            <Card
              key={resume.id}
              className="bg-slate-900/70 border-slate-800 flex flex-col justify-between"
            >
              <CardHeader>
                <CardTitle className="flex items-center justify-between gap-3 text-base">
                  <span className="truncate">{resume.title}</span>
                  <Badge
                    variant="outline"
                    className="border-sky-500/60 text-sky-300 uppercase text-[10px]"
                  >
                    {resume.type}
                  </Badge>
                </CardTitle>
                <CardDescription className="text-xs text-slate-400">
                  Click &quot;Open&quot; to view this resume in a new tab.
                </CardDescription>
              </CardHeader>
              <CardContent className="flex items-center justify-between gap-2 pt-0 pb-4">
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    className="rounded-md border-slate-600 text-slate-100 hover:bg-slate-800"
                    onClick={() => {
                      if (resume.url) window.open(resume.url, "_blank");
                    }}
                  >
                    <ExternalLink className="h-3 w-3 mr-1.5" />
                    Open
                  </Button>

                  <Dialog
                    open={!!editingResume && editingResume.id === resume.id}
                    onOpenChange={(open) => {
                      if (!open) setEditingResume(null);
                    }}
                  >
                    <DialogTrigger asChild>
                      <Button
                        size="sm"
                        variant="outline"
                        className="rounded-md border-slate-600 text-slate-100 hover:bg-slate-800"
                        onClick={() => setEditingResume(resume)}
                      >
                        Update
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="bg-slate-950 border-slate-800">
                      <DialogHeader>
                        <DialogTitle>Update Resume</DialogTitle>
                      </DialogHeader>
                      {editingResume && editingResume.id === resume.id && (
                        <ResumeForm
                          resume={editingResume}
                          onSave={handleResumeSave}
                          onCancel={() => setEditingResume(null)}
                        />
                      )}
                    </DialogContent>
                  </Dialog>
                </div>

                <Button
                  size="icon"
                  variant="ghost"
                  className="text-slate-500 hover:text-red-400 hover:bg-red-950/30"
                  onClick={() => handleResumeDelete(resume.id)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* PROJECTS */}
      <section id="projects" className={sectionClasses}>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50">Featured Projects</h2>
            <p className="text-sm text-slate-400 mt-1">
              Explore work across Data Science, AI & LLMs, Machine Learning, and Data Analytics.
            </p>
          </div>
        </div>

        <Tabs defaultValue="data-science" className="space-y-4">
          <TabsList className="bg-slate-900/80 border border-slate-800">
            <TabsTrigger value="data-science" className="data-[state=active]:bg-sky-600">
              Data Science
            </TabsTrigger>
            <TabsTrigger value="ai-llms" className="data-[state=active]:bg-sky-600">
              AI &amp; LLMs
            </TabsTrigger>
            <TabsTrigger value="machine-learning" className="data-[state=active]:bg-sky-600">
              Machine Learning
            </TabsTrigger>
            <TabsTrigger value="data-analytics" className="data-[state=active]:bg-sky-600">
              Data Analytics
            </TabsTrigger>
          </TabsList>

          {/* Helper for per-tab content */}
          <ProjectsTab
            title="Data Science Projects"
            description="Notebooks, pipelines, and end-to-end DS workflows."
            categoryKey="data-science"
            projects={projectsByCategory["data-science"] || []}
            onUpload={handleProjectUpload}
          />
          <ProjectsTab
            title="AI and LLMs Projects"
            description="LLM apps, prompt engineering, and retrieval pipelines."
            categoryKey="ai-llms"
            projects={projectsByCategory["ai-llms"] || []}
            onUpload={handleProjectUpload}
          />
          <ProjectsTab
            title="Machine Learning Projects"
            description="Classical ML models, MLOps experiments, and model evaluation."
            categoryKey="machine-learning"
            projects={projectsByCategory["machine-learning"] || []}
            onUpload={handleProjectUpload}
          />
          <ProjectsTab
            title="Data Analytics Projects"
            description="Dashboards, reports, and analytics case studies."
            categoryKey="data-analytics"
            projects={projectsByCategory["data-analytics"] || []}
            onUpload={handleProjectUpload}
          />
        </Tabs>
      </section>

      {/* CERTIFICATES */}
      <section id="certificates" className={sectionClasses}>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50">Certificates</h2>
            <p className="text-sm text-slate-400 mt-1">
              Upload and manage your certifications with a professional layout.
            </p>
          </div>

          <label className="inline-flex items-center gap-2 cursor-pointer">
            <input
              type="file"
              multiple
              className="hidden"
              onChange={(e) => handleCertificateUpload(e.target.files)}
            />
            <Button
              size="sm"
              className="rounded-lg bg-sky-600 hover:bg-sky-500 flex items-center gap-2"
            >
              <Upload className="h-4 w-4" />
              Add
            </Button>
          </label>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {certificates.length === 0 && (
            <Card className="bg-slate-900/70 border-slate-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Award className="h-4 w-4 text-sky-400" />
                  No certificates uploaded yet
                </CardTitle>
                <CardDescription className="text-sm text-slate-400">
                  Upload your certificates to view them here. Each file will get a &quot;View
                  Certificate&quot; button.
                </CardDescription>
              </CardHeader>
            </Card>
          )}

          {certificates.map((cert) => (
            <Card key={cert.id} className="bg-slate-900/70 border-slate-800">
              <CardHeader>
                <CardTitle className="flex items-center justify-between text-base">
                  <div className="flex items-center gap-2">
                    <Award className="h-4 w-4 text-sky-400" />
                    <span className="truncate">{cert.name}</span>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent className="flex justify-between items-center pt-0 pb-4">
                <p className="text-xs text-slate-400">
                  Click below to open in a new tab. (Local preview link)
                </p>
                <Button
                  size="sm"
                  variant="outline"
                  className="rounded-md border-slate-600 text-slate-100 hover:bg-slate-800"
                  onClick={() => window.open(cert.url, "_blank")}
                >
                  View Certificate
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* CONTACT */}
      <section id="contact" className={sectionClasses}>
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] items-start">
          <div>
            <h2 className="text-2xl font-semibold text-slate-50 mb-2">Contact</h2>
            <p className="text-sm text-slate-400 mb-6">
              Let&apos;s connect for roles, collaborations, or project discussions.
            </p>

            <div className="grid gap-4 sm:grid-cols-3 mb-6">
              <Card className="bg-slate-900/70 border-slate-800">
                <CardContent className="py-4 flex flex-col gap-2">
                  <div className="inline-flex items-center justify-center h-8 w-8 rounded-lg bg-sky-500/15 border border-sky-500/40">
                    <Mail className="h-4 w-4 text-sky-400" />
                  </div>
                  <p className="text-xs font-medium text-slate-300">Email</p>
                  <a
                    href="mailto:your.email@example.com"
                    className="text-xs text-sky-400 truncate hover:underline"
                  >
                    your.email@example.com
                  </a>
                </CardContent>
              </Card>

              <Card className="bg-slate-900/70 border-slate-800">
                <CardContent className="py-4 flex flex-col gap-2">
                  <div className="inline-flex items-center justify-center h-8 w-8 rounded-lg bg-sky-500/15 border border-sky-500/40">
                    <Linkedin className="h-4 w-4 text-sky-400" />
                  </div>
                  <p className="text-xs font-medium text-slate-300">LinkedIn</p>
                  <a
                    href="https://www.linkedin.com/in/your-linkedin"
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-sky-400 truncate hover:underline"
                  >
                    linkedin.com/in/your-linkedin
                  </a>
                </CardContent>
              </Card>

              <Card className="bg-slate-900/70 border-slate-800">
                <CardContent className="py-4 flex flex-col gap-2">
                  <div className="inline-flex items-center justify-center h-8 w-8 rounded-lg bg-sky-500/15 border border-sky-500/40">
                    <Github className="h-4 w-4 text-sky-400" />
                  </div>
                  <p className="text-xs font-medium text-slate-300">GitHub</p>
                  <a
                    href="https://github.com/your-github"
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-sky-400 truncate hover:underline"
                  >
                    github.com/your-github
                  </a>
                </CardContent>
              </Card>
            </div>

            <Card className="bg-slate-900/80 border-slate-800">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Send className="h-4 w-4 text-sky-400" />
                  Contact Form
                </CardTitle>
                <CardDescription className="text-xs text-slate-400">
                  Form submission is currently mocked and will show a toast notification.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form className="space-y-4" onSubmit={handleContactSubmit}>
                  <div className="space-y-1">
                    <label className="text-xs text-slate-300">Name</label>
                    <Input
                      required
                      placeholder="Your name"
                      value={contactForm.name}
                      onChange={(e) =>
                        setContactForm((f) => ({ ...f, name: e.target.value }))
                      }
                      className="bg-slate-950 border-slate-700 text-sm"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs text-slate-300">Email</label>
                    <Input
                      required
                      type="email"
                      placeholder="you@example.com"
                      value={contactForm.email}
                      onChange={(e) =>
                        setContactForm((f) => ({ ...f, email: e.target.value }))
                      }
                      className="bg-slate-950 border-slate-700 text-sm"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs text-slate-300">Message</label>
                    <Textarea
                      required
                      placeholder="Tell me about your project or opportunity..."
                      rows={4}
                      value={contactForm.message}
                      onChange={(e) =>
                        setContactForm((f) => ({ ...f, message: e.target.value }))
                      }
                      className="bg-slate-950 border-slate-700 text-sm resize-none"
                    />
                  </div>
                  <Button
                    type="submit"
                    className="rounded-lg bg-sky-600 hover:bg-sky-500 w-full sm:w-auto"
                  >
                    Send Message
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          <div className="hidden lg:block">
            <Card className="bg-slate-900/80 border-slate-800 h-full">
              <CardContent className="h-full flex flex-col justify-center gap-4">
                <p className="text-sm text-slate-300">
                  I&apos;m open to internships, entry-level roles, and hands-on projects in:
                </p>
                <ul className="text-xs text-slate-300 space-y-2">
                  <li>• Data Science & Machine Learning</li>
                  <li>• Data Analytics & Business Intelligence</li>
                  <li>• AI / LLM-based product development</li>
                </ul>
                <p className="text-xs text-slate-400">
                  Share a brief context about your requirement, timeline, and tech stack. I&apos;ll
                  get back to you with next steps and availability.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-slate-800 bg-slate-950/95">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>© {new Date().getFullYear()} Pranav Sangichetty. All rights reserved.</p>
          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={() => scrollToSection("hero")}
              className="hover:text-sky-400 transition-colors"
            >
              Back to top
            </button>
            <a
              href="https://github.com/your-github"
              target="_blank"
              rel="noreferrer"
              className="hover:text-sky-400"
            >
              GitHub
            </a>
            <a
              href="https://www.linkedin.com/in/your-linkedin"
              target="_blank"
              rel="noreferrer"
              className="hover:text-sky-400"
            >
              LinkedIn
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

/* ----------------- Subcomponents ----------------- */

function ResumeForm({
  resume,
  onSave,
  onCancel,
}: {
  resume: Resume;
  onSave: (r: Resume) => void;
  onCancel: () => void;
}) {
  const [form, setForm] = React.useState<Resume>(resume);

  return (
    <form
      className="space-y-4 mt-2"
      onSubmit={(e) => {
        e.preventDefault();
        const id = form.id || Date.now();
        onSave({ ...form, id });
      }}
    >
      <div className="space-y-1">
        <label className="text-xs text-slate-300">Title</label>
        <Input
          required
          value={form.title}
          onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
          placeholder="Data Science Resume"
          className="bg-slate-950 border-slate-700 text-sm"
        />
      </div>
      <div className="space-y-1">
        <label className="text-xs text-slate-300">Type (DS, DA, etc.)</label>
        <Input
          required
          value={form.type}
          onChange={(e) => setForm((f) => ({ ...f, type: e.target.value }))}
          placeholder="DS"
          className="bg-slate-950 border-slate-700 text-sm"
        />
      </div>
      <div className="space-y-1">
        <label className="text-xs text-slate-300">Resume URL</label>
        <Input
          required
          value={form.url}
          onChange={(e) => setForm((f) => ({ ...f, url: e.target.value }))}
          placeholder="/resumes/data-science-resume.pdf"
          className="bg-slate-950 border-slate-700 text-sm"
        />
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button
          type="button"
          variant="ghost"
          className="text-slate-400 hover:text-slate-100"
          onClick={onCancel}
        >
          Cancel
        </Button>
        <Button type="submit" className="bg-sky-600 hover:bg-sky-500">
          Save
        </Button>
      </div>
    </form>
  );
}

function ProjectsTab({
  title,
  description,
  categoryKey,
  projects,
  onUpload,
}: {
  title: string;
  description: string;
  categoryKey: string;
  projects: Project[];
  onUpload: (categoryKey: string, files: FileList | null) => void;
}) {
  return (
    <TabsContent value={categoryKey} className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h3 className="text-lg font-medium text-slate-50">{title}</h3>
          <p className="text-xs text-slate-400 mt-1">{description}</p>
        </div>

        <label className="inline-flex items-center gap-2 cursor-pointer">
          <input
            type="file"
            multiple
            className="hidden"
            onChange={(e) => onUpload(categoryKey, e.target.files)}
          />
          <Button
            size="sm"
            variant="outline"
            className="rounded-lg border-slate-600 text-slate-100 hover:bg-slate-800 flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            Upload
          </Button>
        </label>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {projects.length === 0 && (
          <Card className="bg-slate-900/70 border-slate-800">
            <CardHeader>
              <CardTitle className="text-sm text-slate-200">No projects yet</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Upload project files or link your GitHub repositories to populate this section.
              </CardDescription>
            </CardHeader>
          </Card>
        )}

        {projects.map((project) => (
          <Card key={project.id} className="bg-slate-900/80 border-slate-800 flex flex-col">
            <CardHeader>
              <CardTitle className="text-base text-slate-50 truncate">
                {project.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col justify-between gap-3">
              <p className="text-xs text-slate-300">{project.description}</p>
              <div className="flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-wide text-slate-500">
                  {project.link?.startsWith("blob:") || project.link?.startsWith("blob:")
                    ? "Local Upload"
                    : "Linked Project"}
                </span>
                {project.link && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="rounded-md border-slate-600 text-slate-100 hover:bg-slate-800"
                    onClick={() => window.open(project.link, "_blank")}
                  >
                    <ExternalLink className="h-3 w-3 mr-1.5" />
                    Open
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </TabsContent>
  );
}
