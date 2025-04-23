#!/bin/bash

OUTPUT_FILE="/tmp/system_info.txt"
DEBUG_LOG="/tmp/debug.log"

> "$OUTPUT_FILE"
> "$DEBUG_LOG"

echo "System info collected at: $OUTPUT_FILE"

{
  echo "Script started"
  echo "Running as user: $(whoami)"
  echo "Creating system info report..."

  echo "-----------------------------------------------------------"
  echo -n "System Name: ";  uname -n
  echo -n "Date: ";  date
  echo -n "Timezone: "; date | awk '{print $5}'
  echo -n "$(lscpu | sed -n '4p')"
  echo -n "$(cat /proc/meminfo | sed -n '1p')"
  echo "-----------------------------------------------------------"

  echo
  echo "Operating System Information"
  echo "============================"
  cat /etc/os-release 2>/dev/null || lsb_release -a 2>/dev/null

  echo
  echo "Logical Disk Information"
  echo "========================"
  df -Ph | awk '{printf "\t%-25s\t%s\t%s\t%s\t%s\t%s\n",$1,$2,$3,$4,$5,$6}' | grep -vE "/tmp|/var"

  echo
  echo "Mount Points Information"
  echo "========================"
  cat /etc/fstab

  echo
  echo "Service Status:"
  echo "==============="
  if command -v systemctl &> /dev/null; then
    systemctl list-units --type=service --state=running
  else
    echo "Systemctl not found, skipping service status."
  fi

  echo
  echo "/etc Directory Status:"
  echo "======================"
  find /etc -type f -print0 | xargs -0 du -sh 2>> "$DEBUG_LOG"

  echo
  echo "/opt Directory Status:"
  echo "======================"
  find /opt -type f -print0 | xargs -0 du -sh 2>> "$DEBUG_LOG"

  echo
  echo "Ora Mounts Status:"
  echo "=================="
  find /u02 -type f -print0 | xargs -0 du -sh 2>> "$DEBUG_LOG"

  echo
  echo "============================================End of Compliance Report============================================"
} >> "$OUTPUT_FILE" 2>> "$DEBUG_LOG"

echo "✅ Script executed successfully." >> "$OUTPUT_FILE"

