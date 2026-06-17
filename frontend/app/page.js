'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useTheme } from 'next-themes';
import { v4 as uuidv4 } from 'uuid';
import {
  Castle, Search, Mountain, MapPin, Calendar, Droplets, Home,
  Compass, Sparkles, BarChart3, ChevronRight, Sun, Moon, Github,
  Send, Bookmark, ArrowUpRight, RotateCcw,
  Trophy, Loader2, MessageSquareText, ShieldCheck, Layers, History,
  Filter,
} from 'lucide-react';
import {
  ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip as RTooltip,
} from 'recharts';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Slider } from '@/components/ui/slider';
import { toast } from 'sonner';
import { getMeta, getStats, getForts, getSimilarForts, querySemanticSearch } from '@/lib/backend';

const DIFFICULTY_COLOR = {
  Easy: 'bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-900',
  Moderate: 'bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-900',
  Hard: 'bg-rose-100 text-rose-700 border-rose-200 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-900',
};

const TYPE_COLOR = {
  'Hill Fort': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900',
  'Sea Fort': 'bg-sky-50 text-sky-700 border-sky-200 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-900',
  'Land Fort': 'bg-stone-100 text-stone-700 border-stone-300 dark:bg-stone-900 dark:text-stone-300 dark:border-stone-800',
};

const CHART_COLORS = ['#1f8a4c', '#d6a64f', '#5b3a1c', '#31c56f', '#17693a', '#a87d3a', '#6fbb86'];

function classNames(...arr) { return arr.filter(Boolean).join(' '); }

function Header({ tab, setTab }) {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const tabs = [
    { value: 'explore', label: 'Explore', icon: Compass },
    { value: 'recommendations', label: 'Recommendations', icon: Sparkles },
    { value: 'insights', label: 'Insights', icon: BarChart3 },
    { value: 'ai', label: 'AI Guide', icon: MessageSquareText },
  ];

  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between gap-4 px-4 md:px-6">
        <div className="flex items-center gap-2.5">
          <div className="grid h-9 w-9 place-items-center rounded-xl gradient-forest text-white shadow-md shadow-emerald-900/20">
            <Castle className="h-5 w-5" />
          </div>
          <div className="flex flex-col leading-none">
            <span className="text-[15px] font-bold tracking-tight" style={{ fontFamily: "'Playfair Display', serif" }}>
              Pride of Sahyadri
            </span>
            <span className="text-[11px] text-muted-foreground">Maharashtra Forts Heritage</span>
          </div>
        </div>

        <nav className="hidden md:flex">
          <div className="flex items-center gap-1 rounded-full border border-border/70 bg-muted/40 p-1">
            {tabs.map((t) => {
              const Icon = t.icon;
              const active = tab === t.value;
              return (
                <button
                  key={t.value}
                  onClick={() => setTab(t.value)}
                  className={classNames(
                    'relative inline-flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-sm font-medium transition-colors',
                    active ? 'text-emerald-700 dark:text-emerald-300' : 'text-muted-foreground hover:text-foreground',
                  )}
                >
                  {active && (
                    <motion.div
                      layoutId="tab-pill"
                      className="absolute inset-0 rounded-full bg-background shadow-sm border border-border/60"
                      transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                    />
                  )}
                  <Icon className="relative h-3.5 w-3.5" />
                  <span className="relative">{t.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        <div className="flex items-center gap-1.5">
          <Button
            variant="ghost"
            size="icon"
            className="h-9 w-9 rounded-full"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            aria-label="Toggle theme"
          >
            {mounted && (theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />)}
          </Button>
          <Button variant="ghost" size="icon" className="h-9 w-9 rounded-full hidden sm:inline-flex" aria-label="GitHub">
            <Github className="h-4 w-4" />
          </Button>
          <Avatar className="h-9 w-9 ring-2 ring-emerald-200/60 dark:ring-emerald-900/40">
            <AvatarFallback className="bg-gradient-to-br from-emerald-500 to-emerald-700 text-white font-semibold text-xs">
              पS
            </AvatarFallback>
          </Avatar>
        </div>
      </div>

      <div className="md:hidden border-t border-border/60 px-2 pb-2 pt-2 overflow-x-auto">
        <div className="flex items-center gap-1">
          {tabs.map((t) => {
            const Icon = t.icon;
            const active = tab === t.value;
            return (
              <button
                key={t.value}
                onClick={() => setTab(t.value)}
                className={classNames(
                  'inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-colors',
                  active ? 'bg-emerald-600 text-white' : 'bg-muted/60 text-muted-foreground'
                )}
              >
                <Icon className="h-3.5 w-3.5" /> {t.label}
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}

function FilterSelect({ label, value, onChange, options }) {
  return (
    <div>
      <label className="text-xs font-medium text-muted-foreground mb-1.5 block">{label}</label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="h-10 rounded-xl bg-muted/40 border-border/60">
          <SelectValue placeholder={`All ${label.toLowerCase()}`} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All {label.toLowerCase()}</SelectItem>
          {options.map((opt) => (
            <SelectItem key={opt} value={opt}>{opt}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

function Sidebar({ filters, setFilters, meta, applyFilters, resetFilters }) {
  return (
    <aside className="hidden lg:block w-80 shrink-0">
      <div className="sticky top-20 space-y-4">
        <Card className="border-border/60 soft-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Filter className="h-4 w-4 text-emerald-600" /> Filters
            </CardTitle>
            <CardDescription>Refine your fort exploration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-xs font-medium text-muted-foreground mb-1.5 block">Search</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                <Input
                  value={filters.q}
                  onChange={(e) => setFilters((s) => ({ ...s, q: e.target.value }))}
                  placeholder="Name, district, history..."
                  className="pl-9 h-10 rounded-xl bg-muted/40 border-border/60"
                />
              </div>
            </div>

            <FilterSelect label="District" value={filters.district}
              onChange={(v) => setFilters((s) => ({ ...s, district: v }))}
              options={meta?.districts || []} />
            <FilterSelect label="Fort Type" value={filters.type}
              onChange={(v) => setFilters((s) => ({ ...s, type: v }))}
              options={meta?.types || []} />
            <FilterSelect label="Trek Difficulty" value={filters.difficulty}
              onChange={(v) => setFilters((s) => ({ ...s, difficulty: v }))}
              options={meta?.difficulties || []} />
            <FilterSelect label="Best Season" value={filters.season}
              onChange={(v) => setFilters((s) => ({ ...s, season: v }))}
              options={meta?.seasons || []} />
            <FilterSelect label="Water Availability" value={filters.water}
              onChange={(v) => setFilters((s) => ({ ...s, water: v }))}
              options={meta?.waterOptions || []} />

            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="text-xs font-medium text-muted-foreground">Elevation Range</label>
                <span className="text-[11px] text-muted-foreground">{filters.elev[0]}m – {filters.elev[1]}m</span>
              </div>
              <Slider value={filters.elev}
                onValueChange={(v) => setFilters((s) => ({ ...s, elev: v }))}
                min={0} max={1600} step={50} className="py-2" />
            </div>

            <div className="flex gap-2 pt-1">
              <Button onClick={applyFilters} className="flex-1 gradient-forest text-white border-0 hover:opacity-90">
                Apply Filters
              </Button>
              <Button onClick={resetFilters} variant="outline" size="icon" aria-label="Reset">
                <RotateCcw className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60 soft-shadow">
          <CardContent className="p-4">
            <div className="flex items-start gap-3">
              <div className="grid h-9 w-9 place-items-center rounded-lg bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300">
                <Trophy className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-sm font-semibold">Did you know?</h3>
                <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                  Salher Fort (1567 m) is the highest fort in Maharashtra and was the site of the first open-ground Maratha victory over the Mughals in 1672.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </aside>
  );
}

function FortCard({ fort, onView, onSelectForRec }) {
  return (
    <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} whileHover={{ y: -4 }} transition={{ duration: 0.25 }} className="group">
      <Card className="overflow-hidden border-border/60 soft-shadow hover:soft-shadow-lg transition-shadow h-full flex flex-col">
        <div className="relative aspect-[16/9] overflow-hidden">
          <img src={fort.image} alt={fort.name} className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
            <Badge className={classNames('border rounded-full text-[10px] px-2 py-0.5 font-medium', TYPE_COLOR[fort.type] || '')}>{fort.type}</Badge>
            <Badge className={classNames('border rounded-full text-[10px] px-2 py-0.5 font-medium', DIFFICULTY_COLOR[fort.difficulty])}>{fort.difficulty}</Badge>
          </div>
          <div className="absolute bottom-3 left-3 right-3 text-white">
            <h3 className="text-lg font-bold leading-tight" style={{ fontFamily: "'Playfair Display', serif" }}>{fort.name}</h3>
            <div className="flex items-center gap-1 text-xs opacity-95">
              <MapPin className="h-3 w-3" /> {fort.district}
              {fort.elevation > 0 && <><span className="mx-1">·</span><Mountain className="h-3 w-3" /> {fort.elevation}m</>}
            </div>
          </div>
        </div>
        <CardContent className="p-4 flex-1 flex flex-col">
          <p className="text-xs text-muted-foreground line-clamp-3 leading-relaxed flex-1">{fort.summary}</p>
          <div className="flex items-center gap-2 mt-3">
            <Button size="sm" variant="default" className="flex-1 gradient-forest text-white border-0 hover:opacity-90 h-8 text-xs" onClick={() => onView(fort)}>
              View Details <ChevronRight className="h-3 w-3 ml-0.5" />
            </Button>
            <Button size="icon" variant="outline" className="h-8 w-8" onClick={() => onSelectForRec(fort)} aria-label="Find similar">
              <Sparkles className="h-3.5 w-3.5" />
            </Button>
            <Button size="icon" variant="outline" className="h-8 w-8" onClick={() => toast.success(`Bookmarked ${fort.name}`)} aria-label="Bookmark">
              <Bookmark className="h-3.5 w-3.5" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function StatCard({ icon: Icon, label, value, tone }) {
  const tones = {
    emerald: 'from-emerald-500 to-emerald-700',
    amber: 'from-amber-500 to-amber-600',
    brown: 'from-stone-600 to-stone-800',
    forest: 'from-emerald-700 to-emerald-900',
  };
  return (
    <motion.div whileHover={{ y: -2 }} className="rounded-2xl border border-border/60 bg-card/80 backdrop-blur p-4 soft-shadow">
      <div className={classNames('grid h-9 w-9 place-items-center rounded-lg text-white bg-gradient-to-br', tones[tone])}>
        <Icon className="h-4 w-4" />
      </div>
      <div className="mt-3 text-2xl font-bold tabular-nums">{value}</div>
      <div className="text-xs text-muted-foreground">{label}</div>
    </motion.div>
  );
}

function ExplorePage({ forts, loading, onView, onSelectForRec, stats, setTab }) {
  return (
    <div className="space-y-8">
      <div className="relative overflow-hidden rounded-3xl border border-border/60 gradient-hero p-6 md:p-10">
        <div className="absolute -top-20 -right-20 h-72 w-72 rounded-full bg-emerald-400/20 blur-3xl" />
        <div className="absolute -bottom-20 -left-20 h-72 w-72 rounded-full bg-amber-400/20 blur-3xl" />
        <div className="relative grid lg:grid-cols-2 gap-8 items-center">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 dark:border-emerald-900 bg-emerald-50 dark:bg-emerald-950/50 px-3 py-1 text-xs font-medium text-emerald-700 dark:text-emerald-300">
              <ShieldCheck className="h-3.5 w-3.5" /> Heritage exploration platform
            </div>
            <h1 className="mt-4 text-3xl md:text-5xl font-bold tracking-tight leading-tight" style={{ fontFamily: "'Playfair Display', serif" }}>
              Discover Maharashtra's <span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-600 via-emerald-500 to-amber-500">Historic Forts</span>
            </h1>
            <p className="mt-4 text-muted-foreground max-w-xl leading-relaxed">
              Explore over 350+ forts across the Sahyadri mountain ranges — from Shivaji Maharaj's first capital Rajgad to the unconquered sea fort of Murud-Janjira.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Button className="gradient-forest text-white border-0 hover:opacity-90 rounded-xl" size="lg" onClick={() => window.scrollTo({ top: 600, behavior: 'smooth' })}>
                Start Exploring <ArrowUpRight className="h-4 w-4 ml-1" />
              </Button>
              <Button variant="outline" size="lg" className="rounded-xl border-border/70" onClick={() => setTab && setTab('ai')}>
                <Sparkles className="h-4 w-4 mr-1.5" /> Ask the AI Guide
              </Button>
            </div>
          </div>
          <div className="relative">
            <div className="grid grid-cols-2 gap-3">
              <StatCard icon={Castle} label="Total Forts" value={stats?.totals?.totalForts || 0} tone="emerald" />
              <StatCard icon={MapPin} label="Districts" value={stats?.totals?.districtsCovered || 0} tone="amber" />
              <StatCard icon={Mountain} label="Trek Routes" value={stats?.totals?.trekRoutes || 0} tone="brown" />
              <StatCard icon={ShieldCheck} label="Heritage Sites" value={stats?.totals?.heritageSites || 0} tone="forest" />
            </div>
          </div>
        </div>
      </div>

      <div>
        <div className="flex items-end justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "'Playfair Display', serif" }}>Featured Forts</h2>
            <p className="text-sm text-muted-foreground">
              {loading ? 'Loading...' : `${forts.length} fort${forts.length !== 1 ? 's' : ''} matching your filters`}
            </p>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="aspect-[3/4] rounded-2xl bg-muted/40 animate-pulse" />
            ))}
          </div>
        ) : (
          <motion.div layout className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {forts.map((fort) => (
              <FortCard key={fort.id} fort={fort} onView={onView} onSelectForRec={onSelectForRec} />
            ))}
            {forts.length === 0 && (
              <div className="col-span-full py-12 text-center text-sm text-muted-foreground">
                No forts match your filters. Try resetting them.
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}

function MetricMini({ icon: Icon, label, value }) {
  return (
    <div className="rounded-xl border border-border/60 bg-muted/30 p-3">
      <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground"><Icon className="h-3 w-3" /> {label}</div>
      <div className="text-sm font-semibold mt-0.5 truncate">{value}</div>
    </div>
  );
}

function Section({ title, body }) {
  return (
    <div>
      <h3 className="font-semibold text-foreground mb-1.5">{title}</h3>
      <p className="text-muted-foreground">{body}</p>
    </div>
  );
}

function InsightsPage({ forts, stats, selectedFort, setSelectedFort }) {
  if (!selectedFort) return <div className="py-12 text-center text-muted-foreground">Loading...</div>;
  return (
    <div className="space-y-6">
      <Card className="overflow-hidden border-border/60 soft-shadow">
        <div className="grid md:grid-cols-2 gap-0">
          <div className="relative aspect-[16/10] md:aspect-auto overflow-hidden min-h-[280px]">
            <img src={selectedFort.image} alt={selectedFort.name} className="h-full w-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/30 to-transparent" />
            <div className="absolute bottom-4 left-4 right-4 text-white">
              <Badge className="bg-white/20 text-white border-white/30 mb-2 backdrop-blur">{selectedFort.type}</Badge>
              <h2 className="text-3xl md:text-4xl font-bold" style={{ fontFamily: "'Playfair Display', serif" }}>{selectedFort.name}</h2>
              <div className="text-sm flex flex-wrap items-center gap-3 mt-1">
                <span className="inline-flex items-center gap-1"><MapPin className="h-3.5 w-3.5" /> {selectedFort.district}</span>
                {selectedFort.elevation > 0 && <span className="inline-flex items-center gap-1"><Mountain className="h-3.5 w-3.5" /> {selectedFort.elevation}m</span>}
                <span className="inline-flex items-center gap-1"><Compass className="h-3.5 w-3.5" /> {selectedFort.coordinates.lat.toFixed(2)}°N, {selectedFort.coordinates.lng.toFixed(2)}°E</span>
              </div>
            </div>
          </div>
          <div className="p-6 md:p-8 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <Badge className={classNames('rounded-full', DIFFICULTY_COLOR[selectedFort.difficulty])}>{selectedFort.difficulty} Trek</Badge>
                <Select value={selectedFort.id} onValueChange={(id) => setSelectedFort(forts.find(f => f.id === id))}>
                  <SelectTrigger className="w-auto min-w-[180px] h-9 rounded-xl text-xs"><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {forts.map(f => <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground">{selectedFort.summary}</p>
            </div>
            <div className="grid grid-cols-2 gap-3 mt-6">
              <MetricMini icon={Calendar} label="Best Season" value={selectedFort.season} />
              <MetricMini icon={Droplets} label="Water" value={selectedFort.water} />
              <MetricMini icon={Home} label="Stay" value={selectedFort.accommodation} />
              <MetricMini icon={History} label="Era" value="Maratha Empire" />
            </div>
          </div>
        </div>
      </Card>

      <div className="grid lg:grid-cols-3 gap-5">
        <Card className="lg:col-span-2 border-border/60 soft-shadow">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2"><History className="h-4 w-4 text-emerald-600" /> Historical Narrative</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm leading-relaxed">
            <Section title="History" body={selectedFort.history} />
            <Section title="Architecture" body={selectedFort.architecture} />
            <Section title="Strategic Importance" body={selectedFort.strategic} />
            <Section title="Visitor Notes" body={selectedFort.notes} />
          </CardContent>
        </Card>

        <Card className="border-border/60 soft-shadow">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2"><Layers className="h-4 w-4 text-amber-600" /> Fort Types</CardTitle>
            <CardDescription>Distribution across the dataset</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={stats?.byType || []} dataKey="value" nameKey="name" innerRadius={45} outerRadius={75} paddingAngle={2}>
                    {(stats?.byType || []).map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                  </Pie>
                  <RTooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 space-y-1.5">
              {(stats?.byType || []).map((it, i) => (
                <div key={it.name} className="flex items-center gap-2 text-xs">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ background: CHART_COLORS[i % CHART_COLORS.length] }} />
                  <span className="flex-1">{it.name}</span>
                  <span className="font-semibold tabular-nums">{it.value}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        <Card className="border-border/60 soft-shadow">
          <CardHeader>
            <CardTitle className="text-base">Difficulty Distribution</CardTitle>
            <CardDescription>How challenging are the treks?</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats?.byDifficulty || []}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.25} />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis fontSize={12} />
                  <RTooltip cursor={{ fill: 'rgba(31, 138, 76, 0.08)' }} />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {(stats?.byDifficulty || []).map((d, i) => {
                      const colors = { Easy: '#10b981', Moderate: '#f59e0b', Hard: '#f43f5e' };
                      return <Cell key={i} fill={colors[d.name] || CHART_COLORS[i]} />;
                    })}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60 soft-shadow">
          <CardHeader>
            <CardTitle className="text-base">Highest Forts (Elevation)</CardTitle>
            <CardDescription>Top peaks in metres above sea level</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats?.elevations || []} layout="vertical" margin={{ left: 30 }}>
                  <CartesianGrid strokeDasharray="3 3" opacity={0.25} />
                  <XAxis type="number" fontSize={11} />
                  <YAxis type="category" dataKey="name" fontSize={10} width={110} />
                  <RTooltip />
                  <Bar dataKey="elevation" fill="#1f8a4c" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-border/60 soft-shadow">
        <CardHeader>
          <CardTitle className="text-base">District-wise Fort Count</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.byDistrict || []}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.25} />
                <XAxis dataKey="name" fontSize={11} angle={-25} textAnchor="end" height={70} interval={0} />
                <YAxis fontSize={11} />
                <RTooltip />
                <Bar dataKey="value" fill="#d6a64f" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function RecommendationCard({ rec, onCompare }) {
  const { fort, score, reasons } = rec;
  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} whileHover={{ y: -4 }}>
      <Card className="overflow-hidden border-border/60 soft-shadow hover:soft-shadow-lg transition-shadow h-full flex flex-col">
        <div className="relative aspect-[16/9]">
          <img src={fort.image} alt={fort.name} className="h-full w-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
          <div className="absolute top-3 right-3 rounded-full bg-white/95 dark:bg-card/95 px-2.5 py-1 text-xs font-bold text-emerald-700 dark:text-emerald-300 backdrop-blur shadow">
            {score}% Match
          </div>
          <div className="absolute bottom-3 left-3 right-3 text-white">
            <h3 className="font-bold" style={{ fontFamily: "'Playfair Display', serif" }}>{fort.name}</h3>
            <div className="text-xs opacity-95">{fort.district}</div>
          </div>
        </div>
        <CardContent className="p-4 flex-1 flex flex-col">
          <ul className="space-y-1 text-xs flex-1">
            {reasons.map((r) => (
              <li key={r} className="flex items-start gap-1.5 text-muted-foreground">
                <span className="text-emerald-600 mt-0.5">✓</span> {r}
              </li>
            ))}
          </ul>
          <div className="flex gap-2 mt-3">
            <Button size="sm" variant="outline" onClick={onCompare} className="flex-1 h-8 text-xs">Compare</Button>
            <Button size="sm" className="flex-1 h-8 text-xs gradient-forest text-white border-0 hover:opacity-90">View Details</Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

function RecommendationsPage({ forts, selectedFort, setSelectedFort }) {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [compareWith, setCompareWith] = useState(null);

  useEffect(() => {
    let cancel = false;
    async function load() {
      if (!selectedFort) return;
      setLoading(true);
      try {
        const data = await getSimilarForts(parseInt(selectedFort.id, 10), 6);
        if (!cancel) {
          setRecs(data.map((fort) => ({
            fort,
            score: 100,
            reasons: [
              `Same type: ${fort.type}`,
              `Similar difficulty: ${fort.difficulty}`,
              `Elevation: ${fort.elevation}m`,
            ],
          })));
        }
      } catch (error) {
        console.error(error);
        if (!cancel) setRecs([]);
      } finally {
        if (!cancel) setLoading(false);
      }
    }
    load();
    return () => { cancel = true; };
  }, [selectedFort]);

  if (!selectedFort) return <div className="py-12 text-center text-muted-foreground">Loading...</div>;

  return (
    <div className="space-y-6">
      <Card className="overflow-hidden border-border/60 soft-shadow">
        <div className="grid md:grid-cols-[280px_1fr] gap-0">
          <div className="relative aspect-[4/3] md:aspect-auto overflow-hidden min-h-[200px]">
            <img src={selectedFort.image} alt={selectedFort.name} className="h-full w-full object-cover" />
          </div>
          <div className="p-5 md:p-6">
            <div className="text-xs uppercase tracking-widest text-emerald-600 dark:text-emerald-400 font-semibold mb-1">You selected</div>
            <h2 className="text-2xl md:text-3xl font-bold" style={{ fontFamily: "'Playfair Display', serif" }}>{selectedFort.name}</h2>
            <div className="flex flex-wrap items-center gap-2 mt-2">
              <Badge variant="outline" className="rounded-full"><MapPin className="h-3 w-3 mr-1" /> {selectedFort.district}</Badge>
              {selectedFort.elevation > 0 && (
                <Badge variant="outline" className="rounded-full"><Mountain className="h-3 w-3 mr-1" /> {selectedFort.elevation}m</Badge>
              )}
              <Badge className={classNames('rounded-full', DIFFICULTY_COLOR[selectedFort.difficulty])}>{selectedFort.difficulty}</Badge>
              <Badge className={classNames('rounded-full border', TYPE_COLOR[selectedFort.type])}>{selectedFort.type}</Badge>
            </div>
            <p className="text-sm text-muted-foreground mt-3 leading-relaxed">{selectedFort.summary}</p>
            <div className="mt-4">
              <label className="text-xs text-muted-foreground">Switch selected fort</label>
              <Select value={selectedFort.id} onValueChange={(id) => setSelectedFort(forts.find(f => f.id === id))}>
                <SelectTrigger className="mt-1 h-10 rounded-xl bg-muted/40 max-w-xs"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {forts.map(f => <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </Card>

      <div>
        <h3 className="text-xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif" }}>Forts you may also love</h3>
        <p className="text-sm text-muted-foreground mb-4">Based on district, type, difficulty, elevation and season similarity</p>
        {loading ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {Array.from({ length: 6 }).map((_, i) => <div key={i} className="h-56 rounded-2xl bg-muted/40 animate-pulse" />)}
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {recs.map((rec) => (
              <RecommendationCard key={rec.fort.id} rec={rec} onCompare={() => setCompareWith(rec.fort)} />
            ))}
          </div>
        )}
      </div>

      <Sheet open={!!compareWith} onOpenChange={(open) => !open && setCompareWith(null)}>
        <SheetContent className="w-full sm:max-w-xl overflow-y-auto">
          <SheetHeader><SheetTitle>Compare Forts</SheetTitle></SheetHeader>
          {compareWith && (
            <div className="mt-4 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-xl overflow-hidden border border-border/60">
                  <img src={selectedFort.image} alt="" className="w-full h-32 object-cover" />
                  <div className="p-3">
                    <div className="text-[10px] uppercase tracking-wider text-emerald-600 font-semibold">Selected</div>
                    <div className="font-semibold text-sm">{selectedFort.name}</div>
                  </div>
                </div>
                <div className="rounded-xl overflow-hidden border border-border/60">
                  <img src={compareWith.image} alt="" className="w-full h-32 object-cover" />
                  <div className="p-3">
                    <div className="text-[10px] uppercase tracking-wider text-amber-600 font-semibold">Recommended</div>
                    <div className="font-semibold text-sm">{compareWith.name}</div>
                  </div>
                </div>
              </div>
              <div className="rounded-xl border border-border/60 overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-muted/40">
                    <tr><th className="text-left p-2 font-semibold">Attribute</th><th className="text-left p-2 font-semibold">{selectedFort.name}</th><th className="text-left p-2 font-semibold">{compareWith.name}</th></tr>
                  </thead>
                  <tbody>
                    {[
                      ['District', selectedFort.district, compareWith.district],
                      ['Type', selectedFort.type, compareWith.type],
                      ['Difficulty', selectedFort.difficulty, compareWith.difficulty],
                      ['Elevation', `${selectedFort.elevation}m`, `${compareWith.elevation}m`],
                      ['Best Season', selectedFort.season, compareWith.season],
                      ['Water', selectedFort.water, compareWith.water],
                      ['Accommodation', selectedFort.accommodation, compareWith.accommodation],
                    ].map((row) => (
                      <tr key={row[0]} className="border-t border-border/60">
                        <td className="p-2 text-muted-foreground">{row[0]}</td>
                        <td className="p-2 font-medium">{row[1]}</td>
                        <td className="p-2 font-medium">{row[2]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>
    </div>
  );
}

const SUGGESTED_QUESTIONS = [
  'Tell me about Rajgad Fort and its strategic role',
  'Which forts are best for beginner trekkers?',
  'Sea forts near Mumbai I can visit in a weekend',
  'Forts most closely associated with Shivaji Maharaj',
];

function MessageBubble({ m }) {
  const isUser = m.role === 'user';
  return (
    <motion.div initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className={classNames('flex items-start gap-3', isUser && 'flex-row-reverse')}>
      <div className={classNames(
        'grid h-8 w-8 place-items-center rounded-full shrink-0 text-white',
        isUser ? 'bg-gradient-to-br from-amber-500 to-amber-700' : 'gradient-forest'
      )}>
        {isUser ? <span className="text-[11px] font-bold">YOU</span> : <Castle className="h-4 w-4" />}
      </div>
      <div className={classNames(
        'max-w-[78%] rounded-2xl px-4 py-3 text-sm',
        isUser ? 'rounded-tr-md bg-emerald-600 text-white' : 'rounded-tl-md bg-muted/60 text-foreground'
      )}>
        {isUser ? (
          <div className="whitespace-pre-wrap">{m.content}</div>
        ) : (
          <div className="markdown-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </motion.div>
  );
}

function AIGuidePage() {
  const [sessionId] = useState(() => {
    if (typeof window === 'undefined') return uuidv4();
    let id = window.localStorage.getItem('sahyadri_session');
    if (!id) { id = uuidv4(); window.localStorage.setItem('sahyadri_session', id); }
    return id;
  });
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      const viewport = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (viewport) viewport.scrollTop = viewport.scrollHeight;
    }
  }, [messages, loading]);

  async function send(question) {
    const q = (question || input).trim();
    if (!q || loading) return;
    setInput('');
    setMessages((m) => [...m, { role: 'user', content: q }]);
    setLoading(true);
    try {
      const answer = await querySemanticSearch(q);
      setMessages((m) => [...m, { role: 'assistant', content: answer }]);
    } catch (e) {
      setMessages((m) => [...m, { role: 'assistant', content: `**Sorry, something went wrong.** ${e.message}` }]);
      toast.error('AI request failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="relative overflow-hidden rounded-3xl border border-border/60 gradient-hero p-6 md:p-10">
        <div className="absolute -top-20 -right-20 h-72 w-72 rounded-full bg-amber-400/20 blur-3xl" />
        <div className="relative max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full border border-amber-200 dark:border-amber-900 bg-amber-50/80 dark:bg-amber-950/50 px-3 py-1 text-xs font-medium text-amber-700 dark:text-amber-300">
            <Sparkles className="h-3.5 w-3.5" /> Powered by GPT-5 · Retrieval-Augmented
          </div>
          <h1 className="mt-3 text-3xl md:text-4xl font-bold tracking-tight" style={{ fontFamily: "'Playfair Display', serif" }}>
            Ask Anything About Maharashtra Forts
          </h1>
          <p className="mt-3 text-muted-foreground">
            History, trek difficulty, best season, architecture, comparisons — your personal AI guide grounded in a curated heritage knowledge base.
          </p>
        </div>
      </div>

      {messages.length === 0 && (
        <div>
          <div className="text-xs uppercase tracking-widest text-muted-foreground mb-2 font-semibold">Suggested questions</div>
          <div className="grid sm:grid-cols-2 gap-3">
            {SUGGESTED_QUESTIONS.map((q) => (
              <motion.button
                key={q}
                whileHover={{ y: -2 }}
                onClick={() => send(q)}
                className="text-left rounded-2xl border border-border/60 bg-card/80 p-4 hover:border-emerald-500/40 transition-colors group"
              >
                <div className="flex items-start gap-3">
                  <div className="grid h-8 w-8 place-items-center rounded-lg bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 group-hover:bg-emerald-100 dark:group-hover:bg-emerald-900">
                    <Sparkles className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-medium">{q}</div>
                    <div className="text-xs text-muted-foreground mt-0.5">Click to ask the AI guide</div>
                  </div>
                  <ArrowUpRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </motion.button>
            ))}
          </div>
        </div>
      )}

      <Card className="border-border/60 soft-shadow overflow-hidden flex flex-col">
        <ScrollArea className="h-[480px] p-5" ref={scrollRef}>
          <div className="space-y-5">
            <AnimatePresence initial={false}>
              {messages.map((m, i) => <MessageBubble key={i} m={m} />)}
            </AnimatePresence>
            {loading && (
              <div className="flex items-start gap-3">
                <div className="grid h-8 w-8 place-items-center rounded-full gradient-forest text-white shrink-0">
                  <Castle className="h-4 w-4" />
                </div>
                <div className="rounded-2xl rounded-tl-md bg-muted/60 px-4 py-3 flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-3.5 w-3.5 animate-spin" /> Consulting the archives...
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <div className="border-t border-border/60 p-3 bg-muted/30">
          <div className="flex items-end gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }}
              placeholder="Ask about any Maharashtra fort..."
              className="flex-1 h-11 rounded-xl bg-background border-border/60"
              disabled={loading}
            />
            <Button onClick={() => send()} disabled={loading || !input.trim()} className="h-11 rounded-xl gradient-forest text-white border-0 hover:opacity-90 px-4">
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

function App() {
  const [tab, setTab] = useState('explore');
  const [forts, setForts] = useState([]);
  const [allForts, setAllForts] = useState([]);
  const [meta, setMeta] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedFort, setSelectedFort] = useState(null);

  const defaultFilters = useMemo(() => ({
    q: '', district: 'all', type: 'all', difficulty: 'all',
    season: 'all', water: 'all', elev: [0, 1600],
  }), []);
  const [filters, setFilters] = useState(defaultFilters);
  const [appliedFilters, setAppliedFilters] = useState(defaultFilters);

  useEffect(() => {
    async function load() {
      try {
        const [metaRes, statsRes, allFortsRes] = await Promise.all([
          getMeta(),
          getStats(),
          getForts(),
        ]);
        setMeta(metaRes);
        setStats(statsRes);
        setAllForts(allFortsRes);
        if (!selectedFort && allFortsRes?.length) setSelectedFort(allFortsRes[0]);
      } catch (e) { console.error(e); }
    }
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const a = appliedFilters;
        const params = {
          q: a.q || undefined,
          district: a.district !== 'all' ? a.district : undefined,
          type: a.type !== 'all' ? a.type : undefined,
          difficulty: a.difficulty !== 'all' ? a.difficulty : undefined,
          season: a.season !== 'all' ? a.season : undefined,
          water: a.water !== 'all' ? a.water : undefined,
          minElev: a.elev[0],
          maxElev: a.elev[1],
        };
        const results = await getForts(params);
        setForts(results);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [appliedFilters]);

  function applyFilters() { setAppliedFilters(filters); toast.success('Filters applied'); }
  function resetFilters() { setFilters(defaultFilters); setAppliedFilters(defaultFilters); }

  function handleSelectForRec(fort) {
    setSelectedFort(fort);
    setTab('recommendations');
    toast.success(`Finding forts similar to ${fort.name}...`);
  }

  function handleViewFort(fort) {
    setSelectedFort(fort);
    setTab('insights');
  }

  return (
    <div className="min-h-screen bg-background">
      <Header tab={tab} setTab={setTab} />
      <main className="mx-auto max-w-[1600px] px-4 md:px-6 py-6 md:py-8">
        <div className="flex gap-6">
          {(tab === 'explore' || tab === 'insights' || tab === 'recommendations') && (
            <Sidebar
              filters={filters} setFilters={setFilters} meta={meta}
              applyFilters={applyFilters} resetFilters={resetFilters}
            />
          )}
          <div className="flex-1 min-w-0">
            <AnimatePresence mode="wait">
              <motion.div
                key={tab}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.25 }}
              >
                {tab === 'explore' && (
                  <ExplorePage forts={forts} loading={loading} onView={handleViewFort} onSelectForRec={handleSelectForRec} stats={stats} setTab={setTab} />
                )}
                {tab === 'insights' && (
                  <InsightsPage forts={allForts} stats={stats} selectedFort={selectedFort || allForts[0]} setSelectedFort={setSelectedFort} />
                )}
                {tab === 'recommendations' && (
                  <RecommendationsPage forts={allForts} selectedFort={selectedFort || allForts[0]} setSelectedFort={setSelectedFort} />
                )}
                {tab === 'ai' && <AIGuidePage />}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </main>

      <footer className="border-t border-border/60 mt-10">
        <div className="mx-auto max-w-[1600px] px-4 md:px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="grid h-6 w-6 place-items-center rounded-md gradient-forest text-white"><Castle className="h-3 w-3" /></div>
            <span>Pride of Sahyadri · Maharashtra Heritage Platform</span>
          </div>
          <div>Built with curiosity for the forts that shaped Hindavi Swarajya</div>
        </div>
      </footer>
    </div>
  );
}

export default App;
