// Web Audio API POS Sound Synthesizer (100% offline, zero audio files required)

let audioCtx = null

function getAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext
    if (AudioContextClass) {
      audioCtx = new AudioContextClass()
    }
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume().catch(() => {})
  }
  return audioCtx
}

export function isAudioEnabled() {
  const val = localStorage.getItem('pos_sound_enabled')
  return val === null ? true : val === 'true'
}

export function setAudioEnabled(enabled) {
  localStorage.setItem('pos_sound_enabled', enabled ? 'true' : 'false')
}

// Crisp scanner blip / cart item add (1100Hz, 70ms)
export function playBeep() {
  if (!isAudioEnabled()) return
  try {
    const ctx = getAudioContext()
    if (!ctx) return

    const osc = ctx.createOscillator()
    const gain = ctx.createGain()

    osc.type = 'sine'
    osc.frequency.setValueAtTime(1100, ctx.currentTime)
    osc.frequency.exponentialRampToValueAtTime(1350, ctx.currentTime + 0.04)

    gain.gain.setValueAtTime(0.12, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.07)

    osc.connect(gain)
    gain.connect(ctx.destination)

    osc.start(ctx.currentTime)
    osc.stop(ctx.currentTime + 0.075)
  } catch (err) {
    console.debug('Audio playback error:', err)
  }
}

// Cash register celebratory chime (C5 -> E5 -> G5 -> C6 ascending bright bell chord)
export function playChime() {
  if (!isAudioEnabled()) return
  try {
    const ctx = getAudioContext()
    if (!ctx) return

    const notes = [
      { freq: 523.25, time: 0.0, dur: 0.35, vol: 0.14 }, // C5
      { freq: 659.25, time: 0.08, dur: 0.35, vol: 0.16 }, // E5
      { freq: 783.99, time: 0.16, dur: 0.45, vol: 0.18 }, // G5
      { freq: 1046.5, time: 0.24, dur: 0.65, vol: 0.22 }, // C6
    ]

    notes.forEach((note) => {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()

      osc.type = 'triangle'
      osc.frequency.setValueAtTime(note.freq, ctx.currentTime + note.time)

      const start = ctx.currentTime + note.time
      gain.gain.setValueAtTime(0.001, start)
      gain.gain.linearRampToValueAtTime(note.vol, start + 0.015)
      gain.gain.exponentialRampToValueAtTime(0.0001, start + note.dur)

      osc.connect(gain)
      gain.connect(ctx.destination)

      osc.start(start)
      osc.stop(start + note.dur)
    })
  } catch (err) {
    console.debug('Audio chime error:', err)
  }
}

// Low warning buzz for voiding, out-of-stock or deletion (260Hz double tone)
export function playWarning() {
  if (!isAudioEnabled()) return
  try {
    const ctx = getAudioContext()
    if (!ctx) return

    ;[0, 0.11].forEach((delay) => {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()

      osc.type = 'sawtooth'
      osc.frequency.setValueAtTime(220, ctx.currentTime + delay)

      const start = ctx.currentTime + delay
      gain.gain.setValueAtTime(0.08, start)
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.08)

      osc.connect(gain)
      gain.connect(ctx.destination)

      osc.start(start)
      osc.stop(start + 0.085)
    })
  } catch (err) {
    console.debug('Audio warning error:', err)
  }
}
