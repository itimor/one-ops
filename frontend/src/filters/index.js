// set function parseTime,formatTime to filter
export { parseTime, formatTime } from '@/utils'

function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/* 数字 格式化*/
export function numberFormatter(num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

// 格式化时间
export function parseDate(datestr) {
  if (datestr !== undefined) {
    const date = datestr.slice(0, 10)
    const time = datestr.slice(11, 19)
    return date + ' ' + time
  }
}

export function diffDate(date) {
  const d1 = new Date()
  const d2 = new Date(date)
  return Math.round(parseInt(d2 - d1) / 1000 / 60 / 60 / 24)
}

// 菜单
export function menuTypeFilter(val) {
  const Map = {
    1: '模块',
    2: '菜单',
    3: '操作'
  }
  return Map[val]
}

// 按钮
export function operateTypeFilter(val) {
  const Map = {
    'none': '无',
    'add': '新增',
    'del': '删除',
    'update': '编辑',
    'view': '查看',
  }
  return Map[val]
}

// wechat 聊天列表时间
export function chatTime(time, option = null) {
  const d = new Date(time)
  const now = Date.now()

  const diff = (now - d) / 1000

  if (diff < 30) {
    return '刚刚'
  } else if (diff < 3600) {
    // less 1 hour
    return Math.ceil(diff / 60) + '分钟前'
  } else if (diff < 3600 * 24) {
    return Math.ceil(diff / 3600) + '小时前'
  } else if (diff < 3600 * 24 * 2) {
    return '1天前'
  }
  if (option) {
    return parseTime(time, option)
  } else {
    return (
      d.getFullYear() +
      '年' +
      d.getMonth() +
      1 +
      '月' +
      d.getDate() +
      '日'
    )
  }
}

// 取第一个字母并大写
export function AvatarFilter(val) {
  return val.substr(0, 1).toUpperCase()
}

// 按钮
export function ASSET_STATUSFilter(val) {
  const Map = {
    0: '待初始化',
    1: '已使用',
    2: '未使用',
    3: '待下线',
    4: '已下线',
  }
  return Map[val]
}

// 按钮
export function ASSET_TYPEFilter(val) {
  const Map = {
    1: "物理机",
    2: "虚拟机",
    3: "容器",
    4: "网络设备",
    5: "其他设备"
  }
  return Map[val]
}

// 按钮
export function OS_TYPEFilter(val) {
  const Map = {
    1: "centos",
    2: "windows",
    3: "debian",
    4: "other",
  }
  return Map[val]
}

// 按钮
export function STATUS_TYPEFilter(val) {
  const Map = {
    1: "RUNNING",
    2: "RUNNING",
    3: "SUCCESS",
    4: "ABORTED",
    5: "FAILURE",
  }
  return Map[val]
}