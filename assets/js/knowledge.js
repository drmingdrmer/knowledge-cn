const board = document.getElementById('knowledge-board')
const status = document.getElementById('canvas-status')
const url = new URL(window.location.href)

// Full-page mode keeps card links in the address bar and opens notes on this site.
const hasCanvas = url.searchParams.has('canvas')
const hasVault = url.searchParams.has('vault')
if (!hasCanvas) url.searchParams.set('canvas', board.dataset.canvas)
if (!hasVault) url.searchParams.set('vault', board.dataset.vault)
history.replaceState(history.state, '', url)

try {
  const renderer = await import(board.dataset.renderer)
  await renderer.mount(board)
  const collapseObserver = new MutationObserver(changes => {
    for (const change of changes) {
      const card = change.target
      if (card.dataset.enlarged === 'true') continue

      const content = card.querySelector('.canvas-node-content')
      content.scrollTop = 0
    }
  })
  collapseObserver.observe(board.shadowRoot, {
    attributes: true,
    attributeFilter: ['data-enlarged'],
    subtree: true,
  })
  status.hidden = true
} catch (error) {
  status.textContent = `知识地图加载失败：${error.message}。请刷新页面重试。`
  console.error(error)
} finally {
  board.setAttribute('aria-busy', 'false')
}
