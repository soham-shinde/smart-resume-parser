
const BackgroundSVG = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-slate-950" aria-hidden="true">
      <div className="absolute -top-40 -right-40 h-[28rem] w-[28rem] rounded-full bg-primary/20 blur-3xl animate-pulse-slow" />
      <div
        className="absolute -bottom-40 -left-40 h-[24rem] w-[24rem] rounded-full bg-fuchsia-600/10 blur-3xl animate-pulse-slow"
        style={{ animationDelay: "2s" }}
      />
      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            "linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />
    </div>
  );
};

export default BackgroundSVG;
