package com.example.demo.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "用户服务", description = "用户注册/登录认证、基本信息管理")
public class UserController {

    @PostMapping
    @Operation(summary = "用户注册", description = "接收用户名、密码、手机号进行注册")
    public ResponseEntity<Map<String, Object>> register(@RequestBody Map<String, Object> userDto) {
        // 模拟落库操作
        Map<String, Object> response = new HashMap<>();
        response.put("message", "注册成功");
        response.put("userId", 1001);
        response.put("username", userDto.get("username"));
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/login")
    @Operation(summary = "用户登录", description = "验证用户名和密码返回Token")
    public ResponseEntity<Map<String, Object>> login(@RequestBody Map<String, String> credentials) {
        Map<String, Object> response = new HashMap<>();
        if ("zhang".equals(credentials.get("username")) && "123".equals(credentials.get("password"))) {
            response.put("message", "登录成功");
            response.put("token", "mock-jwt-token-xxxxxx");
            return ResponseEntity.ok(response);
        } else {
            response.put("message", "用户名或密码错误");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
        }
    }
}