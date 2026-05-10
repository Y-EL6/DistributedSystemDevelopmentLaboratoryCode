package com.example.demo.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/orders")
@Tag(name = "订单服务", description = "订单创建、订单状态流转管理")
public class OrderController {

    @PostMapping
    @Operation(summary = "创建订单", description = "接收用户ID、地址ID及菜品列表创建新订单")
    public ResponseEntity<Map<String, Object>> createOrder(@RequestBody Map<String, Object> orderDto) {
        // 模拟调用菜品服务扣减库存、创建订单快照
        Map<String, Object> response = new HashMap<>();
        response.put("orderId", "ORD-" + System.currentTimeMillis());
        response.put("status", "UNPAID"); // 对应设计中的待支付状态
        response.put("message", "订单创建成功，请尽快支付");
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{id}")
    @Operation(summary = "查询订单详情", description = "根据订单ID获取订单当前状态与详情")
    public ResponseEntity<Map<String, Object>> getOrder(@PathVariable String id) {
        Map<String, Object> response = new HashMap<>();
        response.put("orderId", id);
        response.put("status", "PAID"); 
        response.put("totalAmount", 88.5);
        response.put("message", "查询成功");
        return ResponseEntity.ok(response);
    }
}